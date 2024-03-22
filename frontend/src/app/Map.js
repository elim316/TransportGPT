import React, { useEffect } from "react";
import { GoogleMap, useJsApiLoader, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "calc(100vw - 40px)",
  height: "100vh",
};

function Map(props) {
  const {
    startPoint,
    endPoint,
    setStartPoint,
    setEndPoint,
    setStartText,
    setEndText,
    focusedTextField,
  } = props;
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
  });

  const [map, setMap] = React.useState(null);
  const [center, setCenter] = React.useState(null);
  const [markers, setMarkers] = React.useState([]);

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

  const handleGeocode = async (latitude, longitude) => {
    try {
      const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
      const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${apiKey}`;

      const response = await fetch(url);
      const data = await response.json();

      if (data.status === "OK") {
        const address = data.results[0].formatted_address;
        console.log("Reverse geocoded address:", address);
        return address;
      } else {
        console.error("Reverse geocoding failed:", data.status);
        return ""; // or any default value
      }
    } catch (error) {
      console.error("Error performing reverse geocoding:", error);
      return ""; // or any default value
    }
  };

  const handleMapClick = (event) => {
    const latitude = event.latLng.lat();
    const longitude = event.latLng.lng();
    console.log("Clicked location:", { latitude, longitude });
    if (focusedTextField === "start") {
      setStartPoint(`${latitude}, ${longitude}`);
      handleGeocode(latitude, longitude)
        .then((address) => {
          // Do something with the address
          console.log(address);
          setStartText(address)
        })
        .catch((error) => {
          console.error(error);
        });
    } else if (focusedTextField === "end") {
      setEndPoint(`${latitude}, ${longitude}`);
      handleGeocode(latitude, longitude)
        .then((address) => {
          // Do something with the address
          console.log(address);
          setEndText(address)
        })
        .catch((error) => {
          console.error(error);
        });
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
