# AWS Rekognition Label Detection Web App

This is a simple web application built with Flask (Python) that allows users to upload an image file. The application then uses the AWS Rekognition service via the Boto3 library to detect labels (objects, scenes, concepts) within the image and displays the results back to the user.

## Features

*   Upload image files (JPG, PNG, JPEG, GIF) through a web interface.
*   Sends the uploaded image to the AWS Rekognition `DetectLabels` API.
*   Displays the detected labels along with their confidence scores and parent categories (if any).
*   Shows the uploaded image on the results page.
*   Provides user feedback through flash messages for errors or warnings.
*   Basic validation for file presence and allowed file types.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1.  **Python:** Python 3.8 or higher installed.
2.  **pip:** Python package installer (usually comes with Python).
3.  **AWS Account:** An active Amazon Web Services account.
4.  **AWS IAM User:** An IAM user configured in your AWS account with:
    *   Programmatic access (Access Key ID and Secret Access Key).
    *   Permissions to use AWS Rekognition. The `AmazonRekognitionReadOnlyAccess` managed policy is often sufficient for `DetectLabels`. For more restrictive permissions, ensure the user has at least the `rekognition:DetectLabels` permission allowed.

## Setup and Installation

1.  **Clone or Download:** Get the project files onto your local machine. If it's a Git repository:
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
    Otherwise, download the `app.py` file and create the `templates` directory with `index.html` inside it.

2.  **Create Virtual Environment:** It's highly recommended to use a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3.  **Activate Virtual Environment:**
    *   **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Dependencies:** Install Flask and Boto3:
    ```bash
    pip install Flask boto3
    ```
    *(Alternatively, if you create a `requirements.txt` file with `Flask` and `boto3` listed, you can run `pip install -r requirements.txt`)*

## Configuration

1.  **AWS Credentials:** Configure your AWS credentials so Boto3 can access your account. The most common way for local development is using the AWS CLI:
    *   Install the AWS CLI if you haven't already.
    *   Run the configure command and enter the Access Key ID and Secret Access Key for the IAM user you created in the Prerequisites:
        ```bash
        aws configure
        ```
        *   `AWS Access Key ID [None]:` YOUR_ACCESS_KEY
        *   `AWS Secret Access Key [None]:` YOUR_SECRET_KEY
        *   `Default region name [None]:` us-east-1 (or your preferred region where Rekognition is available)
        *   `Default output format [None]:` json (or text/table)

    *   Boto3 will automatically pick up these credentials. Other methods include environment variables or IAM roles (if running on EC2, ECS, etc.).

2.  **Flask Secret Key:** For production environments, change the `app.secret_key` in `app.py` to a unique, random, and secret value. The current value `'your_very_secret_key_here'` is **not secure** for production.

## Running the Application

1.  Make sure your virtual environment is activated.
2.  Navigate to the project's root directory (where `app.py` is located).
3.  Run the Flask development server:
    ```bash
    python app.py
    ```
4.  The application will start and typically be accessible at:
    *   `http://127.0.0.1:5001`
    *   `http://localhost:5001`
    *(Note: The code uses port 5001 and binds to `0.0.0.0`, making it accessible from other devices on your local network via your machine's local IP address, e.g., `http://192.168.1.X:5001`)*

## Usage

1.  Open your web browser and navigate to the URL provided when you ran `python app.py` (e.g., `http://127.0.0.1:5001`).
2.  You will see an upload form. Click "Choose File" (or similar) and select an image file (`.png`, `.jpg`, `.jpeg`, `.gif`).
3.  Click the "Аналізувати Зображення" (Analyze Image) button.
4.  The page will reload. If successful, you will see the uploaded image and a list of labels detected by AWS Rekognition below it. If there was an error (e.g., invalid file type, AWS API error), a message will be displayed at the top.

## File Structure
