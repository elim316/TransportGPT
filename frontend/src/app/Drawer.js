import * as React from "react";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import {
  Button,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";

export default function PermanentDrawerLeft(props) {
  const {
    toggleDrawer,
    startPoint,
    endPoint,
    startText,
    setStartText,
    endText,
    setEndText,
    setFocusedTextField,
  } = props;
  const [gptResponse, setGptResponse] = React.useState("");

  const handleClickSearch = (event) => {};

  const handleStartPointFocus = () => {
    setFocusedTextField("start");
    console.log("start");
  };

  const handleEndPointFocus = () => {
    setFocusedTextField("end");
    console.log("end");
  };

  const handleGenerateTravelAdvisory = async () => {
    try {
      const [startLat, startLong] = startPoint.split(",").map(parseFloat);
      const [endLat, endLong] = endPoint.split(",").map(parseFloat);

      const response = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_lat: startLat,
          user_long: startLong,
          dest_lat: endLat,
          dest_long: endLong,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        // Handle the response data here
        console.log(data);
        setGptResponse(data);
      } else {
        console.error("Failed to generate travel advisory");
      }
    } catch (error) {
      console.error("Error generating travel advisory:", error);
    }
  };

  return (
    <Box sx={{ width: 350 }} role="presentation">
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={toggleDrawer(false)}>
            <ListItemIcon>
              <MenuIcon />
            </ListItemIcon>
            <ListItemText primary="TransportGPT" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <FormControl sx={{ margin: "8px 16px" }} variant="outlined" fullWidth>
            <InputLabel htmlFor="outlined-adornment-search">
              Start Point
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-search"
              value={startText || ""}
              onChange={(e) => {
                setStartText(e.target.value);
              }}
              onFocus={handleStartPointFocus}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="search"
                    onClick={handleClickSearch}
                    edge="end"
                  >
                    <SearchIcon color="primary" />
                  </IconButton>
                </InputAdornment>
              }
              label="Start Point"
            />
          </FormControl>
        </ListItem>
        <ListItem disablePadding>
          <FormControl sx={{ margin: "8px 16px" }} variant="outlined" fullWidth>
            <InputLabel htmlFor="outlined-adornment-search">
              End Point
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-search"
              value={endText || ""}
              onChange={(e) => {
                setEndText(e.target.value);
              }}
              onFocus={handleEndPointFocus}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="search"
                    onClick={handleClickSearch}
                    edge="end"
                  >
                    <SearchIcon color="primary" />
                  </IconButton>
                </InputAdornment>
              }
              label="End Point"
            />
          </FormControl>
        </ListItem>
        <ListItem disablePadding>
          <Button
            sx={{ margin: "8px 16px" }}
            fullWidth
            variant="contained"
            onClick={handleGenerateTravelAdvisory}
          >
            Generate a travel advisory
          </Button>
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ margin: "8px 16px" }}>
        <Typography>Optimal Route</Typography>
      </Box>
      <Box sx={{ margin: "8px 16px" }}>
        <Typography>{gptResponse}</Typography>
      </Box>
    </Box>
  );
}
