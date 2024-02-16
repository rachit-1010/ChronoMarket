import "../styles/BrandBox.css";

function BrandBox({ brand, onSelectBrand }) {
  return (
    <div className="brand-box" onClick={() => onSelectBrand(brand)}>
      {brand}
    </div>
  );
}

export default BrandBox;
