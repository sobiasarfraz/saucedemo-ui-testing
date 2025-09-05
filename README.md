# Saucedemo Automated Testing Suite

This repository contains an **end-to-end automated testing suite** for the [**Saucedemo**](https://www.saucedemo.com/) website, built with **Selenium WebDriver** and **Python**. The tests follow the **Page Object Model (POM)** design pattern and use **pytest fixtures** for setup and configuration. The tests are designed to ensure core functionality works across various user types.

---

## Project Overview

The **Saucedemo Automated Testing Suite** automates the testing of key features on the Saucedemo website. It is designed to test a variety of user scenarios, ensuring the site works correctly for different types of users, including both functional and non-functional cases (e.g., broken images, sorting errors).

The test suite covers:
- **Login** functionality with multiple user types, including locked-out users.
- **Inventory Page** validation (images, sorting).
- **Cart Management** (add, remove items, verify cart count).
- **Checkout Process** (form validation, order completion).
- **Logout** (confirm return to the main page).

---

## Requirements

To run the tests, you'll need the following dependencies:

- **Python** 3.1 or higher
- **Selenium** for browser automation
- **pytest** for running the test suite
- **WebDriver** (ChromeDriver, GeckoDriver, etc.) for your browser
- **logging** for test execution logs
- **screenshot_helper** for taking screenshots during test execution

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sobiasarfraz/saucedemo-ui-testing.git
    cd saucedemo-ui-testing
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the corresponding WebDriver for your browser:
   - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

---

## Project Structure

The project follows a **Page Object Model (POM)** design pattern, which means each page of the application is represented by a class containing the methods to interact with the page. This helps to reduce code duplication and makes the test maintenance easier.

\\Saucedemo-project │
#### tests 
- **|----test_full_flow.py** # Main test suite
#### pages 
- **|----login_page.py** 
- **|----inventory_page.py** 
- **|----cart_page.py** 
- **|----checkout_page.py** 
#### conftest.py
#### screenshot_helper.py
#### logging_helper.py
#### requirements.txt
#### README.md




### Page Object Model (POM)

- **Page Object Model**: In this test suite, we follow the Page Object Model (POM) design pattern. Each page of the application (e.g., Login, Inventory, Cart, Checkout) is represented by a separate class under the `/pages` directory. This approach allows us to encapsulate all interactions with the page, such as clicking buttons, entering text, and validating elements, into the page class. This promotes reusability, better code structure, and easier maintenance.

### Fixtures

- **Fixtures**: The test suite makes use of **pytest fixtures** to set up and configure the test environment. Fixtures allow you to create reusable and modular preconditions for tests. These can include browser initialization, user login, and page object instantiation. Fixtures are defined in the `conftest.py` file, which helps reduce redundancy and improves test scalability.

---

## How to Run the Tests

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Saucedemo-Automated-Tests.git
   cd Saucedemo-Automated-Tests
## Install dependencies:

   ```bash
   pip install -r requirements.txt
```   
Ensure that the WebDriver for your browser is installed and placed in a directory that is in your PATH.

Run the tests using pytest:

  ```bash

  pytest --maxfail=1 --disable-warnings -q
```
## Command Options:
- --maxfail=1: Stops the test execution after the first failure.

- --disable-warnings: Suppresses warnings during test execution.

- -q: Runs tests in quiet mode (reduces verbosity).

Screenshots will be taken during the test execution and stored in the /screenshots directory.

## Test Scenarios
The suite tests the following six user types:

- standard_user: A regular user with full access to the site.

- locked_out_user: A user who has been locked out from the site.

- performance_glitch_user: A user experiencing simulated performance issues.

- problem_user: Faces issues with sorting or interacting with elements and completing tasks.

- visual_user: A user with visual glitches simulated.

- error_user: A user encountering general errors.

## Test Flow
Each user scenario follows these steps:

## 1. Login:
- The user logs in with their credentials. 
- If the login is successful, the user is directed to the inventory page. 
- If the login fails (e.g., for a locked-out user), the correct error message is shown.

## 2. Inventory Page:

- Visual Validation: Ensures all images are loaded correctly, and no broken or missing images are present.

- Sorting Issue: Tests that items can be sorted correctly by price (both high to low and low to high). and handle the alert.

- Item Availability: Simulates situations where users can't add items to the cart (e.g., adding more than a few items). Any issue with adding items is logged.

- Item Adding Issue: For certain users,can't add 3rd and 4th item,skip them and add next item.

## 3.Cart Operations:

- Verifies that the correct number of items are added to the cart.

- Removes items from the cart if necessary.

- Confirms that the cart displays the correct number of items after updates.

## 4. Checkout:

- The user fills out the checkout form (first name, last name, and postal code).

- If the form is incomplete (e.g., missing the first name), the appropriate error message is displayed.

- Order Completion: completing the order and confirms whether the user can finish the checkout process successfully.

- Order Failure: For users who cannot complete the order, the issue is logged.

## 5. Logout:

- The user logs out and is redirected to the main page.

## Logging and Debugging
The test suite includes detailed logging at each stage, ensuring clear visibility of the test process. Screenshots are captured at critical points to help with debugging and troubleshooting. The following events are logged:

- Login success or failure.

- Inventory validation (sorting).

- Cart validation (items added/removed).

- Checkout completion and order placement.

- Logout success.

  - Logs are automatically saved in the /logs directory, which is created by logging_helper.py.
  - Screenshots are saved in the /screenshots directory, handled by screenshot_helper.py during test execution.

    - Both directories are generated at runtime — no need to create them manually.

## Test Reports (HTML)
This project generates a detailed HTML report for every test runs using pytest-html.
-  To generate the report locally, run:
  ```bash
       pytest --html=reports/saucedemo_reports.html
   ```
- In GitHub Actions, the report is uploaded as an artifact.

- To view it on GitHub:

  - Go to Actions tab in your repo.

  - Open the latest workflow run.

  - Find Artifacts at the bottom.

  - Download the report artifact (the HTML file).

  - Open it in your browser to see detailed test results.
  
## Continuous Integration (CI)

- This project uses GitHub Actions to run tests automatically on every push and pull request.
- The CI workflow runs the test suite, generates the HTML report.

 The CI configuration is located at:
  ```bash
    .github/workflows/saucedemo.yml
  ```

## Skills Demonstrated

- Automated UI testing with Selenium and Python

- Test design using Page Object Model (POM)

- pytest fixtures and test orchestration

- CI/CD with GitHub Actions

- Test reporting with pytest-html

- Logging and screenshot capture for debugging
  
## License
This project is licensed under the MIT License - see the LICENSE file for details.
 See the [LICENSE](./LICENSE) file for details.
## Final Notes
The Saucedemo Automated Testing Suite was designed to validate critical user flows on the Saucedemo website. It provides coverage for multiple user types, ensuring that the application behaves correctly under different conditions. Each test case is thoroughly logged, and screenshots are captured to assist with debugging in case of failures.

