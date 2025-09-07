import React from "react";

function Filters({ onFilterChange, availableTypes, availableRegions }) {
  const [vesselType, setVesselType] = React.useState("");
  const [region, setRegion] = React.useState("");

  const handleApplyFilters = () => {
    // Lors de l'application des filtres, envoyer les ID pour le type et la région
    onFilterChange({ vesselType: parseInt(vesselType), region });
  };

  return (
    <div className="filters">
      <select
        value={vesselType}
        onChange={(e) => setVesselType(e.target.value)}
      >
        <option value="">Tous les types</option>
        {availableTypes.map((type) => (
          <option key={type.id} value={type.id}>
            {type.description}
          </option>
        ))}
      </select>

      <select value={region} onChange={(e) => setRegion(e.target.value)}>
        <option value="">Toutes les régions</option>
        {availableRegions.map((region, index) => (
          <option key={index} value={region}>
            {region}
          </option>
        ))}
      </select>

      <button onClick={handleApplyFilters}>Appliquer</button>
    </div>
  );
}

export default Filters;