import React from "react"

class Card extends React.Component {
    state = {
        option: ""
    }

    selectOnChange = (event) => {
        const option = event.target.value;
        console.log("Change subtype: " + option);
        this.setState({option: option});
        // want to re-render parent when this updates
        // TODO: make this work this.props.updateTotals();
    }

    getCurrentFromOption = (option) => {
        const types = this.props.card;
        // find the correct subtype object from card
        for (let i in types) {
            if (types[i].subTypeName === option) {
                return types[i];
            }
        }
        return {};
    }

    render() {
        // card is list of subtype objects
        const card = this.props.card;
        let current = this.getCurrentFromOption(this.state.option);
        if (!current) {
            current = card[0];
        }
        console.log("Current " + JSON.stringify(current));
        console.log(this.state.option);
        return (
        <tr>
            <td>{card[0].cardNumber}</td>
            <td>{card[0].name}</td>
            <td>
                <select
                    onChange={this.selectOnChange}
                    value={this.state.option}
                >
                    {
                        card.map(s=> (
                            <option key={Math.random()} value={s.subTypeName}>{s.subTypeName}</option>
                        ))
                    }
                    <option value=""></option>
                </select>
            </td>
            <td className="marketPrice">{current.marketPrice || "None"}</td>
            <td className="lowPrice">{current.lowPrice || "None"}</td>
            <td className="midPrice">{current.midPrice || "None"}</td>
            <td className="highPrice">{current.highPrice || "None"}</td>
            <td><button  onClick={()=> {this.props.remove(card)}}>X</button></td>
        </tr>
    )}
}

export default Card