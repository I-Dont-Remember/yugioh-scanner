import React from "react"

class Card extends React.Component {
    render() {
        const card = this.props.card;
        return (
        <tr>
            <td>{card.number}</td>
            <td>{card.name}</td>
            <td>{card.marketPrice || "None"}</td>
            <td>{card.lowPrice || "None"}</td>
            <td>{card.midPrice || "None"}</td>
            <td>{card.highPrice || "None"}</td>
            <button onClick={()=> {this.props.remove(card)}}>X</button>
        </tr>
     )}
}

export default Card