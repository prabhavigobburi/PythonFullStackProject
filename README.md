# Personalized Skincare Routine Builder


This Flask web application is a personalized skincare routine builder. It connects to a Supabase database to fetch product data based on user input for skin type and primary skin concern. The app then generates a tailored morning and night routine using the recommended products.

## Features
- **Dynamic Routine Generation**: It creates a custom morning and night skincare routine based on the user's selected skin type and primary skin concern.

- **Supabase Integration**: The application connects to a Supabase database to fetch all product information. This means you can easily manage and update your product list directly from the database without changing the application code.

- **Intuitive Interface**: The user interface is clean, modern, and mobile-friendly, built with simple HTML and Tailwind CSS.

## Project Structure


PersonalisedSkincare/
|
|---src/           #core application logic
|    |---logic.py  #Business logic and task
operations   
|    |__db.py      #database operations
|
|---api/           #Backend API
|    |__main.py    #FastAPI endpoints
|
|----frontend/     #Frontend Application
|     |__app.py    #Streamlit web interface
|
|___requirements.txt #Python Dependencies
|
|___README.md      #Project documentation
|
|___.env           #Python variables

## Quick Start


## Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloning)

### 1. clone or Download the project
# Option 1:Clone with Git
git clone <repository-url>

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies

# Install all required Python packages
pip install -r requirements.txt

### 3. Set Up Supabase Database

1.Create a Supabase Project:

2.Create the Tasks table:

- Go to the SQL Editor in your supabase dashboard
- Run this SQL command:

``` sql
CREATE TABLE products (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  skin_types TEXT[],
  concerns TEXT[]
);

```

3. **Get Your Credentials

### 4. Configure Environment Variables

1. Create a `.env` file in the project root

2. Add your Supabase credentials to `.env` :
SUPABASE_URL="https://gdmabhpdovdfntindnyh.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdkbWFiaHBkb3ZkZm50aW5kbnloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwOTgwNjYsImV4cCI6MjA3MzY3NDA2Nn0.nZHvVvN9HaHnmj2AvINxATT91nmTWrTgYhaOaDTtVNo"

### 5. Run the Appilication

### Streamlit Frontend
streamlit run fornend/app.py


### FastAPI Backend

cd api
python main.py


## How to Use

## Technical Details

This application follows a decoupled architecture with a clear separation of concerns between the frontend and backend.

## Frontend-Backend Communication:
 The Streamlit frontend (a web app) acts as a client, making API calls to the FastAPI backend. This is done via standard HTTP requests (e.g., GET, POST) to retrieve or manipulate data.

## Data Flow: 
When a user interacts with the Streamlit interface, a request is sent to the FastAPI backend. The backend receives the request, and the logic.py component performs any necessary business logic or validation. The db.py component then handles the actual interaction with the Supabase PostgreSQL database, performing CRUD (Create, Read, Update, Delete) operations. The response is then returned through the backend to the frontend for display.

## Technologies Used

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (Python REST API)
- **Database**: Supabase (PostgreSQL-based backend-as-a-service)
- **Language**:Python 3.8+

## Key Components

1. **`src/db.py`**: Database operations 
  - Handles all CRUD operations with supabase

2. **`src/logic.py`**: Business logic 
   - Task validation and processing

3. **`api/main.py`**: FastAPI Endpoints

- This component acts as the backend API, defining the routes and endpoints that the frontend uses to communicate with the backend.

- It receives HTTP requests from the Streamlit frontend, calls the appropriate functions in the logic.py component to handle the request, and returns an HTTP response (usually in JSON format).

- It is the public-facing interface of the backend.

4. **`frontend/app.py`**: Streamlit Web Interface

- This component is the user-facing part of the application.

- It handles the presentation layer, creating the forms and displays that users interact with.

- It sends requests to the FastAPI backend when a user submits a form and then renders the routine received in the response.

- It's responsible for the overall user experience and application flow.


## Troubleshooting

## common Issues

1. **"Module not found" errors**
   - Make sure you've installed all dependencies: 
     `pip install -r requirements.txt`
   - check that you're running commands from the correct directory


## Future Enhancements

Ideas for extending this project:

- **User Authentication**: Implement a user authentication system using Supabase Auth. This would allow users to create accounts, save their personalized routines, and have a more customized experience. Each user's routine data could be stored in a separate table, with Row Level Security (RLS) policies to ensure data privacy.

- **Product Ratings and Reviews**: Add the functionality for users to rate and review products. This would require a new reviews table in the Supabase database. The frontend could then display average ratings and user comments, helping others make informed decisions.

- **Dynamic Product Filtering**: Enhance the product recommendation logic. Instead of just filtering by skin type and concern, allow for additional filters such as brand, price range, and specific ingredients. This would make the routine generation even more precise.

- **Visualizations and Data Analysis**: Integrate a Python library like matplotlib or plotly into the Streamlit frontend. You could then visualize data, such as the most popular products, a breakdown of skin types among users, or a trend of common concerns.

## Support

If you encounter any issues or have questions:

- email: prabhavi006@gmail.com
- phone: 9390776424 