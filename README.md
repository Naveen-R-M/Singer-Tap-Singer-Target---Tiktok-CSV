
# tap-tiktok-shop

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls data from **[TikTok Partner Center APIs](https://partner.tiktokshop.com/doc/page/63fd7426715d622a338c4b31?external_id=63fd7426715d622a338c4b31)**
- Extracts the data as json and outputs the schema for each resource to a seperate csv file.
- The outputted csv files can be found inside the **`output/`** folder.

## Setup

Clone this repository

```
git clone https://github.com/Naveen-R-M/Singer-Tap-Singer-Target---Tiktok-CSV.git
```

Create a virtual environment for **tap**

```
python -m venv .envs/tap-tiktok
```

Activate the virtual environment

```
.envs/tap-tiktok/Scripts/activate
```

Install packages

```
pip install -e .
```

Setup the config.json and .env before running

`config.json`

```
{
    "app_key": <your-api-key>,
    "app_secret": <your-app-secret>,
    "access_token": <your-access-token>
}
```

`.env`

```
APP_KEY=<your-api-key>
APP_SECRET=<your-app-secret>
ACCESS_TOKEN=<your-access-token>

```

Run this Repository

```
tap-tiktok-shop -c .\tap_tiktok_shop\config.json | python .\target_csv.py
```

---

Copyright &copy; 2024 | Naveen-R-M
