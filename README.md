# Odoo Customer Feedback & Car Listings Module

##  Project Overview
This module is a technical demonstration of Odoo's capability to handle custom business flows—specifically managing customer feedback for a vehicle listing platform. It was built to explore Odoo 17's ORM, view inheritance, and data relations.

##  Key Features
* **Custom Data Models:** Implements `car.listing` and `customer.feedback` models.
* **Relational Logic:** Links feedback to specific listings with automated average rating calculations.
* **Advanced Views:** Custom Kanban and Tree views for better UX.
* **Security:** Defined Access Control Lists (ACLs) via `ir.model.access.csv`.

##  Technical Stack
* **Backend:** Python 3.10+
* **Framework:** Odoo 17.0 (LTS)
* **Database:** PostgreSQL 15
* **Environment:** Docker & Docker-Compose

##  Installation & Setup
To run this module locally for review:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kfraz93/odoo-customer-feedback.git](https://github.com/kfraz93/odoo-customer-feedback.git)