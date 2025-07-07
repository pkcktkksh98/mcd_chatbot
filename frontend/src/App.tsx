import { useEffect, useState } from "react";
import OutletMap from "./components/OutletMap";
import axios from "axios";
import stateCenters from "./utils/stateCenters";

type Outlet = {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  state:string;
};

const states = Object.keys(stateCenters);

function App() {
  const [selectedState, setSelectedState] = useState("Kuala Lumpur");
  const [outlets, setOutlets] = useState<Outlet[]>([]);
  const [mapCenter, setMapCenter] = useState<[number, number]>(
    stateCenters["Kuala Lumpur"]
  );
  
  console.log(selectedState);
  console.log(mapCenter);

  useEffect(() => {
    const fetchOutlets = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8000/outlets?state=${selectedState}`
        );
        setOutlets(res.data);
        setMapCenter(stateCenters[selectedState]);
      } finally {
      // Always update center regardless of fetch success
      setMapCenter(stateCenters[selectedState]);
      }
    };

    fetchOutlets();
  }, [selectedState]);
  
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>McDonald's KL Outlet Map</h1>
      <div style={{ position: "absolute", top: 10, left: 10, zIndex: 1000 }}>
        <select
          value={selectedState}
          onChange={(e) => setSelectedState(e.target.value)}
        >
          {states.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
      </div>
      <OutletMap outlets={outlets} center={mapCenter} />
    </div>
  );
}

export default App;
