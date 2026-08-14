import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const COLORS = {
    new: "info",
    offer_received: "warning",
    offer_accepted: "warning",
    sold: "success",
    cancelled: "danger",
};

export class StateBadge extends Component {
    static template = "gestion_inmobiliaria.StateBadge";
    static props = { ...standardFieldProps };

    get badgeClass() {
        return `badge text-bg-${COLORS[this.props.record.data[this.props.name]] || "secondary"}`;
    }

    get label() {
        const value = this.props.record.data[this.props.name];
        const selection = this.props.record.fields[this.props.name].selection || [];
        const match = selection.find(([selectionValue]) => selectionValue === value);
        return match ? match[1] : value;
    }
}

registry.category("fields").add("state_badge", { component: StateBadge });
