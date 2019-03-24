import React from 'react'
import Card from "../components/card"
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const styles = {
    table: {
        width: "85%",
        marginLeft: "auto",
        marginRight: "auto"
    }
}

class Deck extends React.Component {

    getSelected = (id) => {
        const displayed = this.props.displayed;
        return displayed[id] || undefined;
    }

    render() {
        const cards = this.props.cards;
        return (
        <Table style={styles.table}>
            <TableHead>
                <TableRow>
                <TableCell>Number</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>SubType</TableCell>
                <TableCell>marketPrice</TableCell>
                <TableCell>lowPrice</TableCell>
                <TableCell>midPrice</TableCell>
                <TableCell>highPrice</TableCell>
                <TableCell></TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
            {cards && cards.map(c => (
                <Card key={c.id} card={c} remove={this.props.removeCard} onChange={this.props.selectOnChange} selected={this.getSelected(c.id)} />
                )
            )}
            </TableBody>
        </Table>
    )}
}

export default Deck