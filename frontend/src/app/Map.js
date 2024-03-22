import React from "react";
import { GoogleMap, useJsApiLoader } from "@react-google-maps/api";

const containerStyle = {
  width: "calc(100vw - 40px)",
  height: "100vh",
};

function Map(props) {
  const { setStartPoint, setEndPoint, focusedTextField } = props;
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
  });

  const [map, setMap] = React.useState(null);
  const [center, setCenter] = React.useState(null);

  const onLoad = React.useCallback(function callback(map) {
    // const bounds = new window.google.maps.LatLngBounds(center);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setCenter({ lat: latitude, lng: longitude });
        map.panTo({ lat: latitude, lng: longitude });
      },
      (error) => {
        console.error("Error getting user location:", error);
      }
    );

    map.setZoom(15);
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null);
  }, []);

  const handleMapClick = (event) => {
    const latitude = event.latLng.lat();
    const longitude = event.latLng.lng();
    console.log("Clicked location:", { latitude, longitude });
    // check which textfield is focused and set the respective latlong
    if (focusedTextField === "start") {
      setStartPoint(`${latitude}, ${longitude}`);
    } else if (focusedTextField === "end") {
      setEndPoint(`${latitude}, ${longitude}`);
    }
  };


  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={17}
      onLoad={onLoad}
      onUnmount={onUnmount}
      onClick={handleMapClick}
    >
      {/* Child components, such as markers, info windows, etc. */}
      <></>
    </GoogleMap>
  ) : (
    <></>
  );
}

export default React.memo(Map);
