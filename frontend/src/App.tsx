import { useEffect, useState } from "react";
import OutletMap from "./components/OutletMap";
import axios from "axios";


type Outlet = {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
};

function App() {
  const [outlets, setOutlets] = useState<Outlet[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/outlets").then((res) => {
      setOutlets(res.data);
    });
  }, []);

  return (
    <div>
      <h1 style={{ textAlign: "center" }}>McDonald's KL Outlet Map</h1>
      <OutletMap outlets={outlets} />
    </div>
  );
}

export default App;
