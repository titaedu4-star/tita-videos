# Timetable video

A small GitHub Pages website to play and download the edited MP4. No Cloudflare account or storage keys are required.

## Enable the website

In this repository, go to **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main** and **/ (root)**, then **Save**. Wait for deployment to finish; GitHub displays the website URL on that page.

For a repository named `tita-videos` owned by `titaedu4-star`, the default URL is https://titaedu4-star.github.io/tita-videos/.

GitHub Pages is available for public repositories on GitHub Free; private repository availability depends on the account plan. A public repository makes the video accessible to everyone.

## Preview locally

Run `python3 -m http.server 8080` in this folder, then open the local server in your browser. The HTML page and video use relative URLs so the same files work on GitHub Pages.

To replace the video, upload a new `timetable-edited.mp4`. Update the duration shown in `index.html` if it changes.
