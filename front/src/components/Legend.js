import React from 'react';
import disseases from "../assets/js/disseases";
import { Typography, Dialog, ListItem, List } from "@material-ui/core";

function Legend(props) {
  return (
    <Dialog onClose={() => props.setOpen(false)} open={props.open}>
      <List>
        {
          Object.keys(disseases)
            .map((key) => (
              <ListItem key={key}>
                <Typography><b>{key}</b> - {disseases[key]}</Typography>
              </ListItem>
            ))
        }
      </List>
    </Dialog>
  );
}

export default Legend;