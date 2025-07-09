import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useState } from "react";
import { useMapEvent } from "react-leaflet";
import RecenterMap from "../map/RecenterMap";

// Fix default icon issue in Leaflet
import iconUrl from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

// Default (blue) icon
const defaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Yellow icon for nearby outlets
const yellowIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Blue icon for selected outlet
const blueIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

type Outlet = {
  id: number;
  name: string;
  address: string;
  lat: number;
  lng: number;
};

type Props = {
  outlets: Outlet[];
  center: [number, number];
};

export default function OutletMap({ outlets,center }: Props) {
  const [selectedOutlet, setSelectedOutlet] = useState<Outlet | null>(null);
  const [nearbyOutlets, setNearbyOutlets] = useState<number[]>([]);
  // console.log(center);

  // Helper: Calculate distance in KM using Haversine
  const getDistanceInKm = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const handleMarkerClick = (outlet: Outlet) => {
    setSelectedOutlet(outlet);

    // Find other outlets within 5KM
    const nearby = outlets
      .filter((o) => o.id !== outlet.id)
      .filter(
        (o) =>
          getDistanceInKm(outlet.lat, outlet.lng, o.lat, o.lng) <= 5
      )
      .map((o) => o.id);

    setNearbyOutlets(nearby);
  };

  function MapClickHandler({ onClick }: { onClick: () => void }) {
        useMapEvent("click", () => {
            onClick();
        });
        return null;
    }


  return (
    <MapContainer center={center} zoom={12} style={{ height: "80vh"}}>
      <RecenterMap center={center} />
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    <MapClickHandler onClick={() => {
        setSelectedOutlet(null);
        setNearbyOutlets([]);
        }} />

      {outlets.map((outlet) => {
        let icon = defaultIcon;
        if (selectedOutlet?.id === outlet.id) {
          icon = blueIcon;
        } else if (nearbyOutlets.includes(outlet.id)) {
          icon = yellowIcon;
        }

        return (
          <Marker
            key={outlet.id}
            position={[outlet.lat, outlet.lng]}
            icon={icon}
            eventHandlers={{ click: () => handleMarkerClick(outlet) }}
          >
            <Popup>
              <strong>{outlet.name}</strong>
              <br />
              {outlet.address}
            </Popup>
          </Marker>
        );
      })}

      {selectedOutlet && (
        <Circle
          center={[selectedOutlet.lat, selectedOutlet.lng]}
          radius={5000}
          pathOptions={{ color: "blue", fillColor: "blue", fillOpacity: 0.2 }}
        />
      )}
    </MapContainer>
  );
}
