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
    startText,
    setStartText,
    endText,
    setEndText,
    setFocusedTextField,
  } = props;

  const handleClickSearch = (event) => {};

  const handleStartPointFocus = () => {
    setFocusedTextField("start");
    console.log("start");
  };

  const handleEndPointFocus = () => {
    setFocusedTextField("end");
    console.log("end");
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
          <Button sx={{ margin: "8px 16px" }} fullWidth variant="contained">
            Generate a travel advisory
          </Button>
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ margin: "8px 16px" }}>
        <Typography>Optimal Route</Typography>
      </Box>
    </Box>
  );
}
