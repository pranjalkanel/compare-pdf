import requests

def download_pdf(url, save_path):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF downloaded successfully and saved to {save_path}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

if __name__ == "__main__":
    pdf_url = "https://www.africau.edu/images/default/sample.pdf"  # Replace with the actual PDF URL
    save_path = "downloaded_file.pdf"  # Specify the desired save path

    download_pdf(pdf_url, save_path)
