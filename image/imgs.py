import os

def rename_images_sequentially(folder_path):
    """
    Renames all image files in a folder sequentially (1.jpg, 2.png, etc.).

    Args:
        folder_path (str): The path to the folder containing the images.
    """
    try:
        files = sorted(os.listdir(folder_path))  # Get sorted list of files
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))] #filter for image file types

        if not image_files:
            print(f"No image files found in {folder_path}")
            return

        for index, old_name in enumerate(image_files):
            file_extension = os.path.splitext(old_name)[1]
            new_name = f"{index + 1}{file_extension}"
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed '{old_name}' to '{new_name}'")

        print("Image renaming completed.")

    except FileNotFoundError:
        print(f"Error: Folder not found at {folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")  # Get folder path from user
    rename_images_sequentially(folder_path)
