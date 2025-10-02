import os
import requests

def download_dataset(zip_url, folder_path):
    """
    Here, we download the Patch Dataset from remote if it does not already exist on disk, as specified by TRAINING_DATASET_DIR.
    """

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"{folder_path} does not exist. Downloading ZIP from {zip_url}...")

        # Stream the download and write to a file
        with requests.get(zip_url, stream=True) as response:
            response.raise_for_status()  # Check for HTTP errors
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024 * 1024 * 128 # 128 MB

            # Write to a temp file for large size
            with tqdm(total=total_size//(1024*1024), unit='MB', unit_scale=True, desc='Downloading') as progress_bar:
                temp_zip_path = "temp_download.zip"
                with open(temp_zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # Filter out keep-alive chunks
                            file.write(chunk)
                            progress_bar.update(len(chunk)//(1024*1024))


        # extract the ZIP file
        print("Extracting the files...")
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)

        # remove the zip file after extraction
        os.remove(temp_zip_path)
        print(f"Content extracted to {folder_path}.")
    else:
        print(f"{folder_path} already exists. No need to download.")
