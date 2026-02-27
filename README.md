# About

Experimental app for learning about FastAPI (deployed on Render - and/or perhaps Railway and Fly... og even Vercel) and for exploring the potential role of FastAPI in the Rollo stack, e.g.:
1. As a secondary backend that implements features (notably web sockets) that the primary  Anvil backend does not support. 
   - The client app would decide which backend to use depending on the situation (nicely wrapped inside the `server` parcel).
   - The Anvil backend would not be aware of FastAPI backend.
   - The FastAPI backend could perhaps have access the targets in the Anvil backend via a (likely client) Uplink connection or via `requests` (or any )
2. As "pseudo monolith" where
   - The FastAPI app serves the document (and thereby escapes cors issues), which in turns embeds the Anvill app's frontend as an iframe to take advantage of Anvil's user services.
   - The Vercel-deployed client app only serves static assets (and acts as a test space and - as a repo - is home to parcels).
   - The Anvil app's backend mainly acts as a db host and perhaps some special Anvil RPC/http endpoint targets that can be called from either JS or the FastAPI app.