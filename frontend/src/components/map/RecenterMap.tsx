import { useEffect } from "react";
import { useMap } from "react-leaflet";

type Props = {
  center: [number, number];
};

export default function RecenterMap({ center }: Props) {
  const map = useMap();

  useEffect(() => {
    map.flyTo(center, map.getZoom());
  }, [center, map]);

  return null;
}
