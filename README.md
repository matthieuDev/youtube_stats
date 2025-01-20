# youtube_stats

A Python project designed to analyze YouTube channel statistics by retrieving video data and generating graphs to visualize the evolution of video views over time.

## Project Structure

### 1. **`api_querier.py`**
   - Defines the `youtube_querier_class` for interacting with the YouTube Data API.
   - Features methods to:
     - Retrieve channel IDs using a channel handle.
     - Fetch video lists for a specific channel.
     - Obtain detailed statistics for videos.
     - Collect and save all video information for a given channel in a JSON file.

### 2. **`create_graph.py`**
   - Contains the `create_view_graph` function for generating scatter plots.
   - Visualizes the evolution of video views over time using a logarithmic scale for better representation of large datasets.

### 3. **`path_folder.py`**
   - Initializes folder paths for storing data, dumps, and graphs.
   - Ensures that required directories (`data/`, `dumps/`, `graphs/`) exist, creating them if necessary.

### 4. **`main.py`**
   - Entry point for the project.
   - Retrieves video data for a specified YouTube channel and generates a graph showing the evolution of views over time.
   - Usage: 
     ```bash
     python main.py <channel_name>
     ```

## API key

For the project to run you need an API key. Once obtained you need to create a `secret_keys.py` contianing the key in a variable. Use `secrets_keys.example.py` as the template.

## Output
- Data Dumps: JSON files containing detailed video statistics saved in the data/dumps/ folder.
- Graphs: Scatter plots showing video views over time saved in the data/graphs/ folder.

## Requirements

Python 3.x

Libraries: googleapiclient, matplotlib