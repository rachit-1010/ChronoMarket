import "../styles/Items.css";
import { useNavigate } from "react-router-dom";
function Items({ items, error }) {
  const navigate = useNavigate();
  const handleSearchSubmit = async () => {
    try {
      const endpoint = `http://localhost:3500/api/item/search?query=${searchQuery}`;
      const response = await makeApiRequest("GET", endpoint);

      if (response.success) {
        setItems(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    }
  };
  return (
    <div className="items-container">
      {error && <p>Error: {error}</p>}
      {items.map((item, index) => (
        <div
          key={index}
          className="item"
          onClick={() => {
            navigate(`/user/bid/${item.id}`);
          }}
        >
          <img
            src={
              item.item_image
                ? `data:image/jpg;base64,${item.item_image}`
                : "https://dehayf5mhw1h7.cloudfront.net/wp-content/uploads/sites/1075/2019/03/16192350/No-Photo-Provided.png"
            }
            alt={item.name}
            className="watch-image"
          />
          <p>Name: {item.item_name}</p>
          <p>Watch Model: {item.watch_model}</p>
        </div>
      ))}
    </div>
  );
}

export default Items;
