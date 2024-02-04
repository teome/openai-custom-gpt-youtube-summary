# OpenAI Custom GPT Setup With Modal FastAPI Endpoint For YouTube Summarisation

This is a simple but effective configuration setup for a custom GPT that has access to an endpoint, hosted via Modal, with a FastAPI app with a single endpoint a YouTube URL.

The app then downloads the first 30 min of the video and uses the Whisper API to transcribe the audio. The GPT then has access to this content, prints a summary to you and allows for a conversation from then on about any subjects related to it.

## Modal setup
You'll need paid access to ChatGPT and a Modal account with credits (there are free credits on signup). Once you have the Modal account setup add your OPENAI_API_KEY as a secret. This secret is referenced in the Modal FastAPI app as `agents_modal00` but change this as needed. The cost for running this on Modal is very low a it's just CPU, a little disk usage and API accesses. That said, I'm not running a version for you to play with!

## GPT setup

Follow the custom GPTs setup flow that's integrated into the create/edit GPT workflow, accessed from ChatGPT. You can follow the questions that the system asks, or simply copy in the config that I made:

```
As YouTubeTranscriber and Commentary, your primary role is to assist users in obtaining transcriptions of YouTube videos and providing expert-level commentary. When a user provides a YouTube URL, utilize the transcription tool to generate the video's text, ensuring accuracy and clarity. Should the user request commentary, tailor your analysis to their guidance. If no specific direction is given, independently analyze the transcript, focusing on potentially intriguing aspects.

For topics involving medicine, pharmacology, or neuroscience, base your web searches on credible sources such as PubMed, scientific journals, and Reddit discussions. Steer clear of personal blogs for these areas. When the `journal-reddit-cross-reference` command is issued, compare and contrast information from scientific and public domains to provide a comprehensive view.

Your audience comprises experts in fields like physics, AI, neuroscience, and pharmacology. Engage them with insightful, scientific commentary, leveraging your web browsing, DALL-E, and code interpreter skills. Remember, your users are knowledgeable, so there's no need to shy away from complex topics or suggest consulting other experts.
```

Add the following JSON schema for the endpoint in the GPT Agent configuration. Note that the schema can be retrieved any time from `<URL>/openapi.json` but you'll need to add the `server` section which the Agent configuration requires.

```json
{"openapi":"3.0.2","info":{"title":"FastAPI","version":"0.1.0"},
  "servers": [
    {
      "url": "https://<YOUR URL FOR THE API ENDPOINT>"
    }
  ],
"paths":{"/":{"post":{"summary":"Transcribe Video","description":"Download audio from the YouTube video and transcribe it using OpenAI's Whisper model","operationId":"transcribe_video__post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/VideoRequest"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}},"components":{"schemas":{"HTTPValidationError":{"title":"HTTPValidationError","type":"object","properties":{"detail":{"title":"Detail","type":"array","items":{"$ref":"#/components/schemas/ValidationError"}}}},"ValidationError":{"title":"ValidationError","required":["loc","msg","type"],"type":"object","properties":{"loc":{"title":"Location","type":"array","items":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"msg":{"title":"Message","type":"string"},"type":{"title":"Error Type","type":"string"}}},"VideoRequest":{"title":"VideoRequest","required":["url"],"type":"object","properties":{"url":{"title":"Url","type":"string"}}}}}}
```

## Modal API endpoint access without GPT

You can also access your running endpoint easily like so:

```
curl \
    -X POST https://<YOUR_MODAL_URL>/transcribe \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.youtube.com/watch?v=<SUPER_INTERESTING_VID_ID>"}'
```

That's it. This is an example to get up and running, there's lots more that can be integrated with other API access.