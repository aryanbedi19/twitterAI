# TwitterAI

## Overview
TwitterAI is a Flask-based web application designed to automate interactions with Twitter using the OpenAI API. This project allows users to post tweets, delete tweets, and retrieve user profile information through a user-friendly web interface. The integration with OpenAI's powerful AI models enables advanced features like generating tweet content dynamically or responding to commands in natural language.

## Features
- **Tweet Posting**: Automatically post tweets to a connected Twitter account.
- **Tweet Deletion**: Remove tweets from a connected Twitter account.
- **Profile Information**: Fetch and display profile information from the Twitter API.
- **AI-Enhanced Interactions**: Use OpenAI's models to interpret user commands and perform actions accordingly.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework.
- **OpenAI API**: Leveraging AI models for processing natural language commands.
- **OAuth1**: Authentication protocol for secure API requests to Twitter.
- **Requests-OAuthlib**: Library for OAuth1 authentication with Python requests.

## Usage
Navigate to the various endpoints (`/post_tweet`, `/delete_tweet`, `/profile`) to interact with Twitter through the web interface or use the `/command` endpoint for AI-driven interactions.
