# telegram-dl-bot-example

## Introduction
This is an example workflow of building a telegram DL inference bot. 
You can implement this bot with your bot token and do inference using mnist dataset.

## Prefilght check

- [ ] Get the Bot token from telegram bot father([link](https://t.me/botfather)).
- [ ] Configure you token by changing the setting in `config.ini`.

## Installation
Run this code before you install the dependencies using following command:
```
pip3 install -r requirement.txt
```

## Run bot
You may run this bot by using following command:
```
python3 main.py
```
And feel free to interupt it using `ctrl + c`.

## Structure of Inference workflow

```mermaid
sequenceDiagram
    TG Client ->>+ TG Server: Send `/prediect` request by reply to some image.
    TG Server ->>+ Self-hosting Bot: Got a `/prediect` request.
    Self-hosting Bot ->>+ TG Server: Request image that `/predict` command replied to.
    TG Server ->>+ Self-hosting Bot: Send request image.
    Self-hosting Bot ->>+ Inference Module: Send inference request with tranformed image.
    Inference Module ->>+ Self-hosting Bot: Return inference result.  
    Self-hosting Bot -->>+ TG Server: Return inference result with message and photo.  
    TG Server -->>+ TG Client: Return inference result with message and photo.  
    
```
