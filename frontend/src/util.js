export const formatDate = (dateTypeVar) => {
  const formattedDate =
    dateTypeVar.getFullYear() +
    "-" +
    ("0" + (dateTypeVar.getMonth() + 1)).slice(-2) +
    "-" +
    ("0" + dateTypeVar.getDate()).slice(-2) +
    " " +
    ("0" + dateTypeVar.getHours()).slice(-2) +
    ":" +
    ("0" + dateTypeVar.getMinutes()).slice(-2) +
    ":" +
    ("0" + dateTypeVar.getSeconds()).slice(-2);
  return formattedDate;
};
