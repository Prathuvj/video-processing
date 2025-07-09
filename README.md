# Video Processing Application

## Uses

This application is designed to process video files by providing functionalities such as format conversion, metadata extraction, thumbnail generation, video resizing, and trimming.

## Setup Instructions

1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment using `python -m venv venv`.
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install the dependencies using `pip install -r requirements.txt`.

## Run Instructions

1. Ensure the virtual environment is activated.
2. Run the application using `python app.py`.

## Technical Decisions and Implementation

The application is structured to separate concerns across different modules, each handling a specific aspect of video processing. This modular approach enhances maintainability and scalability.

## Challenges Faced with Gradio and Choice of Streamlit

Initially, Gradio was considered for creating the user interface due to its simplicity and ease of use for quick prototyping. However, challenges such as Dependency issues with other libraries and integration capabilities led to the decision to switch to Streamlit. Streamlit offers more flexibility and compatibilty for prototyping interactive and visually appealing web applications.

## Improvements for the Future

- Enhance the UI with more interactive elements and better design.
- Add support for additional video formats and processing options.
- Implement more robust error handling and logging mechanisms to improve reliability.
