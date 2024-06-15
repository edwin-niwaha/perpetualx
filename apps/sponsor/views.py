from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.child.models import Child

from .forms import (
    ChildSponsorshipForm,
    SponsorDepartForm,
    SponsorForm,
)
from .models import (
    ChildSponsorship,
    Sponsor,
    SponsorDeparture,
)


# =================================== Sponsors List ===================================
@login_required
def sponsor_list(request):
    queryset = Sponsor.objects.all().filter(is_departed="No").order_by("id")

    search_query = request.GET.get("search")
    if search_query:
        queryset = queryset.filter(first_name__icontains=search_query).filter(last_name__icontains=search_query)

    paginator = Paginator(queryset, 25)  # Show 25 records per page
    page = request.GET.get("page")

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)

    return render(
        request,
        "main/sponsor/sponsor_details.html",
        {"records": records, "table_title": "Sponsors MasterList"},
    )

# =================================== Register Sponsor ===================================

@login_required
@transaction.atomic
def register_sponsor(request):
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.info(
                request, "Record saved successfully!", extra_tags="bg-success"
            )
            return redirect("register_sponsor") 
        else:
            # Display form errors
            return render(request, "main/sponsor/sponsor_register.html", {"form": form})
    else:
        form = SponsorForm()
    return render(
        request,
        "main/sponsor/sponsor_register.html",
        {"form_name": "Sponsor Registration", "form": form},
    )

# =================================== Update Sponsor data ===================================
@login_required
@transaction.atomic
def update_sponsor(request, pk, template_name="main/sponsor/sponsor_register.html"):
    try:
        sponsor_record = Sponsor.objects.get(pk=pk)
    except Sponsor.DoesNotExist:
        messages.error(request, "Record not found!")
        return redirect("sponsor_list")  # Or a relevant error page

    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES, instance=sponsor_record)
        if form.is_valid():
            form.save()

            messages.success(request, "Record updated successfully!")
            return redirect("sponsor_list") 
    else:
        # Pre-populate the form with existing data
        form = SponsorForm(instance=sponsor_record)

    context = {"form_name": "Sponsor Registration", "form": form}
    return render(request, template_name, context)


# =================================== Deleted selected Sponsor ===================================
@login_required
@transaction.atomic
def delete_sponsor(request, pk):
    records = Sponsor.objects.get(id=pk)
    records.delete()
    messages.info(request, "Record deleted successfully!", extra_tags="bg-danger")
    return HttpResponseRedirect(reverse("sponsor_list"))


# =================================== Depart Sponsor ===================================
@login_required
@transaction.atomic
def sponsor_departure(request):
    if request.method == "POST":
        form = SponsorDepartForm(request.POST, request.FILES)
        if form.is_valid():
            sponsor_id = request.POST.get("id")
            sponsor_instance = get_object_or_404(Sponsor, pk=sponsor_id)

             # Create a sponsorDepart instance
            sponsor_depart = SponsorDeparture.objects.create(sponsor=sponsor_instance)
            sponsor_depart.departure_date = form.cleaned_data["departure_date"]
            sponsor_depart.departure_reason = form.cleaned_data["departure_reason"]
            sponsor_depart.save()

            # Update sponsor status to "departed"
            sponsor_instance.is_departed = "Yes"
            sponsor_instance.save()

            messages.success(request, "Sponsor departed successfully!")
            return redirect("sponsor_departure")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = SponsorDepartForm()

    sponsors = Sponsor.objects.filter(is_departed="No").order_by("id") 
    return render(
        request,
        "main/sponsor/sponsor_depature.html",
        {"form": form, "form_name": "Sponsors Depature Form", "sponsors": sponsors},
    )

# =================================== sponsor Depature Report ===================================
def sponsor_depature_list(request):
    queryset = Sponsor.objects.all().filter(is_departed="Yes").order_by("id").prefetch_related("departures")

    search_query = request.GET.get("search")
    if search_query:
        queryset = queryset.filter(first_name__icontains=search_query).filter(last_name__icontains=search_query)

    paginator = Paginator(queryset, 25)  # Show 10 records per page
    page = request.GET.get("page")

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)

    return render(
        request,
        "main/sponsor/sponsor_depature_list.html",
        {"records": records, "table_title": "Departed Sponsors"},
    )

# =================================== Reinstate departed sponsor ===================================
@login_required
@transaction.atomic
def reinstate_sponsor(request, pk):
    sponsor = get_object_or_404(Sponsor, id=pk)
    
    if request.method == 'POST':
        sponsor.is_departed = "No"
        sponsor.save()
        messages.success(request, "Sponsor reinstated successfully!")

        return redirect("sponsor_depature_list")
    
    return render(request, 'main/sponsor/sponsor_depature_list.html', {'sponsor': sponsor})


# =================================== Child Sponsorship ===================================
@login_required
@transaction.atomic
def child_sponsorship(request):
    if request.method == "POST":
        form = ChildSponsorshipForm(request.POST, request.FILES)
        if form.is_valid():
            sponsor_id = request.POST.get("sponsor_id") 
            child_id = request.POST.get("child_id") 
            sponsor_instance = get_object_or_404(Sponsor, pk=sponsor_id)
            child_instance = get_object_or_404(Child, pk=child_id)

            # Check if sponsorship already exists
            existing_sponsorship = ChildSponsorship.objects.filter(
                sponsor=sponsor_instance, 
                child=child_instance).exists()
            if existing_sponsorship:
                messages.error(request, "Sponsorship already exists for this child and sponsor.")
            else:
                try:
                    # Create the sponsorship instance
                    with transaction.atomic():
                        sponsorship = ChildSponsorship.objects.create(sponsor=sponsor_instance, child=child_instance)
                        sponsorship.sponsorship_type = form.cleaned_data["sponsorship_type"]
                        sponsorship.start_date = form.cleaned_data["start_date"]
                        sponsorship.save()

                        # Update sponsor status to "departed"
                        child_instance.is_sponsored = "Yes"
                        child_instance.save()

                    messages.success(request, "Submitted successfully!")
                    return redirect("child_sponsorship")
                except IntegrityError:
                    # Handle integrity error if any
                    messages.error(request, "An error occurred while processing the request.")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = ChildSponsorshipForm()

    children = Child.objects.filter(is_departed="No").order_by("id")  
    sponsors = Sponsor.objects.filter(is_departed="No").order_by("id") 
    return render(
        request,
        "main/sponsor/child_sponsorship.html",
        {"form": form, "form_name": "Child Sponsorship", "sponsors": sponsors, "children": children},
    )

# =================================== Child Sponsorship Report ===================================
@login_required
def child_sponsorship_report(request):
    if request.method == "POST":
        child_id = request.POST.get("id")
        if child_id:
            selected_child = get_object_or_404(Child, id=child_id)
            child_sponsorship = ChildSponsorship.objects.filter(child_id=child_id)
            children = Child.objects.all().filter(is_departed="No").filter(is_sponsored="Yes").order_by("id")
            return render(request, 'main/sponsor/child_sponsorship_rpt.html', 
                          {"table_title": "Child Sponsorship Report", "children": children, 
                           "child_name": selected_child.full_name, "prefix_id":selected_child.prefixed_id, 
                           'child_sponsorship': child_sponsorship})
        else:
            messages.error(request, "No child selected.")
    else:
        children = Child.objects.all().filter(is_departed="No").filter(is_sponsored="Yes").order_by("id")
    return render(request, 'main/sponsor/child_sponsorship_rpt.html', 
                    {"table_title": "Child Sponsorship Report", "children": children})


# =================================== Delete Sponsorship Data ===================================
@login_required
@transaction.atomic
def delete_child_sponsorship(request, pk):
    records = ChildSponsorship.objects.get(id=pk)
    records.delete()
    messages.info(request, "Record deleted successfully!", extra_tags="bg-danger")
    return HttpResponseRedirect(reverse("child_sponsorship_report"))

# =================================== Terminate Child Sponsorship ===================================
@login_required
@transaction.atomic
def terminate_child_sponsorship(request, pk):
    child = get_object_or_404(Child, id=pk)
    
    if request.method == 'POST':
        child.is_sponsored = "No"
        child.save()
        messages.success(request, "Sponsorship terminated successfully!")

        return redirect("child_sponsorship_report")
    
    return render(request, 'main/sponsor/child_sponsorship_rpt.html', {'child': child})