# sgvd-maps

## Example usage

Go to https://openrouteservice.org/ for your API key.

```bash
$ curl "https://sgvd-maps.herokuapp.com/map?key=YOUR_OWN_API_KEY&latS=51.075824&lonS=5.262364&latE=50.927683&lonE=5.386107"
```

```json
{
    "distance" : "33.6",
    "duration" : "32.7",
    "html_map" : "html page"
}
```