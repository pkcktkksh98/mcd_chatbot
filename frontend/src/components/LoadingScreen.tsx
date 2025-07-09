import { ClipLoader } from "react-spinners";

export default function LoadingScreen() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-white">
      <ClipLoader color="#4caf50" size={60} />
      <p className="mt-4 text-gray-600 text-lg">Loading McDonald's Assistant...</p>
    </div>
  );
}
