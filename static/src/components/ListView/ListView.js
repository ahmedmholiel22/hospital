/* @odoo-module */

import { component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ListViewAction extends component {
    static template = "hospital.ListView";
}

registry.category('actions').add("hospital.action_list_view", ListViewAction);