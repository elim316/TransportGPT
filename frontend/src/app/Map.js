import React, { useEffect } from "react";
import { GoogleMap, useJsApiLoader, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "calc(100vw - 40px)",
  height: "100vh",
};

function Map(props) {
  const { startPoint, endPoint, setStartPoint, setEndPoint, focusedTextField } = props;
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
  });

  const [map, setMap] = React.useState(null);
  const [center, setCenter] = React.useState(null);
  const [markers, setMarkers] = React.useState([
    // { lat: startPoint, lng:startPoint },
    // { lat: endPoint, lng:endPoint },
  ]);

  useEffect(() => {
    if (startPoint) {
      // Parse startPoint string into separate latitude and longitude values
      const [startLat, startLng] = startPoint.split(",").map(parseFloat);
      // Update the markers state with the parsed latitude and longitude values for startPoint
      setMarkers((prevMarkers) => {
        const updatedMarkers = [...prevMarkers];
        updatedMarkers[0] = { lat: startLat, lng: startLng };
        return updatedMarkers;
      });
    }
  }, [startPoint]);
  
  useEffect(() => {
    if (endPoint) {
      // Parse endPoint string into separate latitude and longitude values
      const [endLat, endLng] = endPoint.split(",").map(parseFloat);
      // Update the markers state with the parsed latitude and longitude values for endPoint
      setMarkers((prevMarkers) => {
        const updatedMarkers = [...prevMarkers];
        updatedMarkers[1] = { lat: endLat, lng: endLng };
        return updatedMarkers;
      });
    }
  }, [endPoint]);

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
      setMarkers
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
      {markers.map((marker, index) => (
        <Marker key={index} position={{ lat: marker.lat, lng: marker.lng }} />
      ))}
    </GoogleMap>
  ) : (
    <></>
  );
}

export default React.memo(Map);
