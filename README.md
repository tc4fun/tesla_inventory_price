# Tesla Inventory Price Check

## To setup

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Setting

```yml
tesla_url: 'https://www.tesla.com/inventory/new/my?TRIM=LRAWD&arrangeby=plh&zip=08550&range=200&referral=tao125473'
sender_email: sender_email@gmail.com
sender_password: app_password # of sender_email@gmail.com check this: https://support.google.com/mail/answer/185833?hl=en
receipient_list: # list of email receivers
  - receiver@gmail.com
poll_interval_sec: 30 # poll every 30 second
price_threshold: 47500 # if price is lower than this, send email
```

`tesla_url` is the url you put in the browser to search tne inventory, you can use your own URL, with correct filters selected.

`sender_password` is the app password of sender_email@gmail, not the gmail password, following the [link](https://support.google.com/mail/answer/185833?hl=en) to create one.

`price_threshold` is the limit when a lower price is find, the script will send an email to the `recerver@gmail.com` address

You can use my referring link, which gives you 6 month free super charging and 3 month free FSD: https://www.tesla.com/referral/tao125473

