import React from "react"
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

class Card extends React.Component {
    getPricesObject = (option) => {
        const prices = this.props.card.prices;
        if (!option) {
            return prices[0];
        }

        for (let i in prices) {
            if (prices[i].subTypeName === option) {
                return prices[i];
            }
        }

        console.log("failed to find matching subtype for " + JSON.stringify(option));
        return prices[0];
    }

    render() {
        // card is list of subtype objects
        const card = this.props.card;
        const selected = this.getPricesObject(this.props.selected);
        return (
        <TableRow>
            <TableCell>{card.cardNumber}</TableCell>
            <TableCell>{card.name}</TableCell>
            <TableCell>
                <select
                    onChange={(event) => {this.props.onChange(event, card.id)}}
                    value={selected.subTypeName}
                >
                    {
                        card.subTypes.map(s=> (
                            <option key={Math.random()} value={s}>{s}</option>
                        ))
                    }
                </select>
            </TableCell>
            <TableCell className="marketPrice">$ {selected.marketPrice || "None"}</TableCell>
            <TableCell className="lowPrice">$ {selected.lowPrice || "None"}</TableCell>
            <TableCell className="midPrice">$ {selected.midPrice || "None"}</TableCell>
            <TableCell className="highPrice">$ {selected.highPrice || "None"}</TableCell>
            <TableCell><IconButton  onClick={()=> {this.props.remove(card.id)}}><DeleteIcon /></IconButton></TableCell>
        </TableRow>
    )}
}

export default Card