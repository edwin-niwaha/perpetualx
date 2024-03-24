import datetime
from datetime import date

from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# =================================== CHILD MODEL ===================================
def current_year():
    return timezone.now().year


class Child(models.Model):
    # Basic info
    full_name = models.CharField(
        max_length=50,
        verbose_name="Full Name",
        validators=[
            RegexValidator(
                r"^[A-Za-z]+(?:\s[A-Za-z]+)*$", "Only letters and spaces are allowed"
            )
        ],
    )
    preferred_name = models.CharField(
        max_length=50, verbose_name="Preferred Name", null=True, blank=True
    )
    residence = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Current Residence"
    )
    district = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Home District"
    )
    tribe = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=False, verbose_name="Gender"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth",
        validators=[
            MinValueValidator(limit_value=datetime.date(year=1900, month=1, day=1)),
            MaxValueValidator(limit_value=datetime.date.today()),
        ],
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Weight in kilograms",
    )
    height = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name="Height in centimeters",
    )

    aspiration = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Aspiration"
    )
    c_interest = models.TextField(
        max_length=100, null=True, blank=True, verbose_name="Interest and abilities "
    )

    # Child Progress details
    SCHOOL_CHOICES = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    is_child_in_school = models.CharField(
        max_length=3, choices=SCHOOL_CHOICES, default="No"
    )

    # Sponsorship info - Foreign table for sponsorship apart from is_sponsored field
    SPONSORSHIP_CHOICES = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    is_sponsored = models.CharField(
        max_length=3,
        choices=SPONSORSHIP_CHOICES,
        default="No",
        verbose_name="Is the child sponsored?",
    )

    # SPONSORSHIP_TYPE_CHOICES = (
    #     ('Full', 'Full Sponsorship'),
    #     ('Co', 'Co-Sponsorship'),
    # )
    # sponsorship_type = models.CharField(
    #     max_length=20, choices=SPONSORSHIP_TYPE_CHOICES, null=True, blank=True, verbose_name="Type of sponsorship")

    # Family background
    # Parents
    father_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Father’s Name"
    )
    is_father_alive = models.CharField(
        choices=(("Yes", "Yes"), ("No", "No")),
        max_length=3,
        verbose_name="Is the father alive?",
    )
    father_description = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="if not what happened/if alive what is happening?",
    )
    mother_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Mother’s name"
    )
    is_mother_alive = models.CharField(
        choices=(("Yes", "Yes"), ("No", "No")),
        max_length=3,
        verbose_name="is the mother alive?",
    )
    mother_description = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="if not what happened/if alive what is happening?",
    )
    # Guardian
    guardian = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Current guardian"
    )
    guardian_contact = PhoneNumberField(
        null=True, blank=True, default="+256999999999", verbose_name="Guardian Contact"
    )
    relationship_with_guardian = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Relationship with the Guardian",
    )
    # Foreign table for siblings relations
    siblings = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="List names and age of the siblings",
    )

    background_info = models.TextField(
        blank=True, null=True, verbose_name="Other family back ground information"
    )
    health_status = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="General health status"
    )
    responsibility = models.TextField(
        max_length=50, null=True, blank=True, verbose_name="Child’s responsibilities"
    )
    relationship_with_christ = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Relationship with Christ"
    )

    RELIGION_CHOICES = (
        ("Born-again Christian", "Born-again Christian"),
        ("Anglican", "Anglican"),
        ("Catholic", "Catholic"),
        ("Muslim", "Muslim"),
    )
    religion = models.CharField(
        max_length=50,
        choices=RELIGION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Religion of the Child",
    )
    prayer_request = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Prayer needs/request"
    )
    YEAR_MAX = current_year()
    year_enrolled = models.IntegerField(
        validators=[MinValueValidator(2013), MaxValueValidator(YEAR_MAX)],
        verbose_name="The year when the child was enrolled on the program?",
    )
    DEPATURE_CHOICES = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    is_departed = models.CharField(
        max_length=3,
        choices=DEPATURE_CHOICES,
        default="No",
        verbose_name="Is the child departed?",
    )

    # Other fields
    staff_comment = models.TextField(
        max_length=50, null=True, blank=True, verbose_name="Staff Comment "
    )
    compiled_by = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Compiled by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "child_info"
        verbose_name = "Child Bio Data"
        verbose_name_plural = "Children Bio Data"

    def __str__(self):
        return self.full_name + " " + self.preferred_name

    @property
    def prefixed_id(self):
        return f"P-0{self.pk}"

    def calculate_age(self):
        today = date.today()
        age = (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age


# =================================== CHILD PROFILE PICTURES MODEL ===================================


class ChildProfilePicture(models.Model):
    child = models.OneToOneField(
        Child, on_delete=models.CASCADE, related_name="profile_picture"
    )
    picture = models.ImageField(
        upload_to="child_profiles/",
        verbose_name="Upload Image(jpg, jpeg, png)",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=False, verbose_name="Is Current Picture")

    class Meta:
        db_table = "child_profile_pictures"
        verbose_name = "Child Profile Picture"
        verbose_name_plural = "Child Profile Pictures"
        ordering = ["-uploaded_at"]
        unique_together = ("child", "picture")

    def __str__(self):
        return f"Profile picture of {self.child.name} uploaded at {self.uploaded_at}"


# =================================== CHILD PROGRESS MODEL ===================================


class ChildProgress(models.Model):
    child = models.ForeignKey(
        "Child", on_delete=models.CASCADE, related_name="progresses"
    )
    name_of_school = models.CharField(
        max_length=50, verbose_name="Name of the School", null=True
    )
    previous_schools = models.TextField(
        max_length=50, blank=True, verbose_name="Previous Schools Attended"
    )
    EDUC_LEVEL_CHOICES = [
        ("Pre-School", "Pre-School"),
        ("Kindergarten", "Kindergarten"),
        ("Primary", "Primary"),
        ("Secondary", "Secondary"),
        ("Tertiary", "Tertiary"),
        ("University", "University"),
    ]
    education_level = models.CharField(
        choices=EDUC_LEVEL_CHOICES,
        default="Pre-School",
        verbose_name="Level of Education",
    )
    CLASS_LEVEL_CHOICES = [
        ("", "Select Class"),  # Default option
        ("Baby", "Baby"),
        ("Middle", "Middle"),
        ("Top", "Top"),
        ("P.1", "Primary One"),
        ("P.2", "Primary Two"),
        ("P.3", "Primary Three"),
        ("P.4", "Primary Four"),
        ("P.5", "Primary Five"),
        ("P.6", "Primary Six"),
        ("P.7", "Primary Seven"),
        ("S.1", "Form One"),
        ("S.2", "Form Two"),
        ("S.3", "Form Three"),
        ("S.4", "Form Four"),
        ("S.5", "Form Five"),
        ("S.6", "Form Six"),
        ("Tertiary", "Tertiary"),
        ("University", "University"),
    ]
    child_class = models.CharField(
        max_length=30,
        choices=CLASS_LEVEL_CHOICES,
        verbose_name="Class",
        blank=True,
        null=True,
    )
    best_subject = models.CharField(
        max_length=30, verbose_name="Best Subject", blank=True, null=True
    )
    score = models.IntegerField(verbose_name="Score (Optional)", blank=True, null=True)
    co_curricular_activity = models.CharField(
        max_length=50, verbose_name="Co-curricular Activity", blank=True, null=True
    )
    responsibility_at_school = models.CharField(
        max_length=50,
        verbose_name="Responsibility at School (Optional)",
        blank=True,
        null=True,
    )
    future_plans = models.TextField(
        max_length=50, verbose_name="Future Plans (Optional)", blank=True, null=True
    )
    responsibility_at_home = models.TextField(
        verbose_name="Responsibility at Home (Optional)", blank=True, null=True
    )
    notes = models.TextField(max_length=50, verbose_name="Notes", blank=True, null=True)

    class Meta:
        db_table = "child_progress"
        verbose_name = "Child Progress"
        verbose_name_plural = "Children Progress"

    def __str__(self):
        return f"{self.child.full_name} - {self.name_of_school}"


# =================================== SPONSOR MODEL ===================================
# class Sponsor(models.Model):
#     DEPATURE_CHOICES = (
#         ('Yes', 'Yes'),
#         ('No', 'No'),
#     )
#     GENDER_CHOICES = (
#     ('Male', 'Male'),
#     ('Female', 'Female'),
#     )
#     sponsor_id = models.AutoField(primary_key=True, verbose_name="Sponsor ID")
#     first_name = models.CharField(max_length=100, null=True, verbose_name="First Name")
#     last_name = models.CharField(max_length=100, null=True, verbose_name="Last Name")
#     gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False,
#                                 verbose_name="Gender")
#     email = models.EmailField(verbose_name="Email")
#     job_title = models.CharField(max_length=100, null=True, verbose_name="Job Title")
#     region = models.CharField(max_length=100, null=True, verbose_name="Region")
#     town = models.CharField(max_length=100, null=True, verbose_name="Town")
#     origin = models.CharField(max_length=100, null=True, verbose_name="Origin")
#     business_telephone = PhoneNumberField(null=True, blank=True, default="+256999999999",
#                                     verbose_name="Business Telephone")
#     mobile_telephone = PhoneNumberField(null=True, blank=True, default="+256999999999",
#                                     verbose_name="Mobile Telephone")

#     city = models.CharField(max_length=100, null=True, verbose_name="City")
#     start_date = models.DateField( null=True, blank=True,
#                                 verbose_name="Start Date",
#                                 validators=[
#     MinValueValidator(limit_value=datetime.date(year=2013, month=1, day=1)),
#     MaxValueValidator(limit_value=datetime.date.today())])
#     comment = models.CharField(max_length=100, null=True, verbose_name="Comment")
#     first_street_address = models.CharField(max_length=100, null=True, verbose_name="First Street Address")
#     second_street_address = models.CharField(max_length=100, null=True, verbose_name="Second Street Address")
#     zip_code = models.CharField(max_length=100, null=True, verbose_name="ZIP Code")
#     is_departed = models.CharField(
#         max_length=3, choices=DEPATURE_CHOICES, default='No', verbose_name="Is the sponsor departed?")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         managed = True
#         db_table = 'sponsor_details'
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# # =================================== SPONSORSHIP TYPE MODEL ===================================
# class SponsorshipType(models.Model):
#     name = models.CharField(max_length=100)
#     amount_to_donate = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         managed = True
#         db_table = 'sponsorship_types'
#     def __str__(self):
#         return f"{self.name}"

# # =================================== SPONSORSHIP MODEL ===================================
# class Sponsorship(models.Model):
#     sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsorships')
#     child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='sponsored_by')
#     sponsorship_type = models.ForeignKey(SponsorshipType, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'sponsorship_details'
#         unique_together = (('child', 'sponsor'),)

#     def __str__(self):
#         return f"{self.child} sponsored by {self.sponsor}"
