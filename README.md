# inda-ckan-homeproject

A web page that interact with data.gov.il CKAN API in order to show selected *gov-data*.

## 1. Install
in order to tun this project you need to clone in locally and then run it on your local achine.

## 2. The App
After running the project go to `http://127.0.0.1:your-app-port/home/` an you will land on the main page.

You will see a form that shows the fields:

- Tag selector - in order to select 1 of 10 most refferenced tags on the API
- Dataset selector - based on the previous tag selection a list of all taged datasets
- Fields selector - a multi-select component in order to choose the dataset fields to select
- Submit button - in order to get the data
- Show query button - in order to show the query string to the API
- Download file - a button that downloads the data as a CSV/XLSX (based on the user's choice

