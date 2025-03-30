# ytsummaryapi

Summarise YouTube videos to spend less time watching them.

## Running the API

You will need to grab your own Gemini API key from
[aistudio.google.com](aistudio.google.com). Once you have it, put it in an
environment variable called `GEMINI_API_KEY` so it can be retrieved by the
application.

To run the server you will need to install the requirements, listed in
`requirements.txt`, whichever way you prefer. This includes `uvicorn` which is
the web server that will host the endpoints.

The endpoint is simply `/summarise/<video_id>`, where `<video_id>` refers to the
UUID after the last `/` in a `youtu.be` URL, or after the `?watch=` in a typical
YouTube URL.

Frontend coming soon.
