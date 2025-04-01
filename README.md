Online Fitness Application System Using Django

Project Overview:


The Online Fitness Application  System is a Django-based web application designed to provide an online platform for fitness vendors and customers. This system allows vendors to upload their fitness plans and manage subscriptions, while customers can browse workout plans, place subscriptions, track progress, and make payments.

The system also provides administrative capabilities for managing the entire platform, including user accounts, subscription plans, payments.
Technologies Used:

-----------------

- Python 3.9.20

- Django 3.

- DynomoDB (for database management)

- AWS Elastic Beanstalk (for deployment)

- AWS Services (SNS notifications and messaging)
 
Features:

---------

Vendor Portal:

Allows vendors to manage their fitness plans, view customer subscriptions, and update subscription statuses.

Customer Portal:

Allows customers to browse available fitness plans, subscribe to workout plans, and track their progress.

Admin Dashboard:

Allows administrators to manage users, view subscription details, and perform administrative tasks (e.g., approving vendors, managing plans).

Subscription Management:

Integrated subscription system to track customer subscriptions, renewals, and cancellations.

Payment Integration:

Integrates payment flow to confirm subscriptions and sends confirmation emails to customers using AWS SNS.

Elastic Beanstalk Deployment:

The project is deployed on AWS Elastic Beanstalk for easy scalability, load balancing, and management.

Real-time Notifications:

AWS SNS is used to send real-time notifications like subscription confirmations, reminders, and workout updates.


 
Project Setup:

--------------

1. Clone the repository:

    git clone <repository_url>
 
2. Set up a virtual environment:

    python3 -m venv venv source venv/bin/activate # On Windows, use myenv\bin\activate

It's recommended to set up a virtual environment to manage the project's dependencies:  
 
3. Install dependencies:

pip install -r requirements.txt
 
Install the required dependencies by running the following:

4. Database Setup:

The project uses DynomoDB by default. To set up the database.
 
5. Create a Superuser (Admin):

To access the admin dashboard, create a superuser by running:

python manage.py createsuperuser
 
7. **Deploy to AWS Elastic Beanstalk**:

- Ensure you have the AWS Elastic Beanstalk CLI installed.

- Set up your Elastic Beanstalk environment using the following command:

eb create <environment_name> --service-role <service_role> --instance_profile <instance_profile>
 
 
AWS Integration:

-----------------

This application is integrated with AWS services such as:

- AWS SNS: For sending notifications (e.g., subcription confirmations, alerts).
 
File Structure:

---------------
Fitness/
    ├── Fitness/                # Core application code
    ├── customers/              # Customer-related functionality (e.g., registration, subscriptions, profiles)
    ├── vendorPortal/           # Vendor-related functionality (e.g., menu management, order tracking)
    ├── static/                 # Static files (CSS, JavaScript, images for the front end)
    ├── templates/              # HTML templates for the front end (pages like home, about, etc.)
    ├── requirements.txt        # List of dependencies for the project
    ├── manage.py               # Django project management script (e.g., runserver, migrate, etc.)
    ├── deploy.py               # Script for deploying to Elastic Beanstalk
    ├── README.md               # Project documentation (this file provides an overview)


----------------

- ALLOWED_HOSTS: Ensure the correct domain name (e.g., Elastic Beanstalk URL) is added to `ALLOWED_HOSTS` in `settings.py` for proper deployment.
 
- Security: Be sure to implement proper security measures, such as SSL/TLS for production deployments, and keep sensitive keys secure.
 
