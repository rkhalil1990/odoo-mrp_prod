
from openerp import api, models
import logging


def div_qty(qty):
    half = qty / 2
    return half

class hr_report(models.AbstractModel):
    _name = 'report.mrp_prod.mrp_prod_record_qweb'








    @api.multi
    def render_html(self, data=None):
        report = self.env['report']._get_report_from_name('mrp_prod.mrp_prod_record_qweb')

        logging.warning(" iam here")
        # logging.warning(self._ids)

        res="my name is ramadan"
        # categories_ids = self.search([]).mapped('record_cat')

        records_ids=self.env['mrp.production.record'].browse(self._ids)
        logging.warning(records_ids)
        dep_ids=records_ids.mapped('record_dep')
        emp_ids=records_ids.mapped('employee_id')
        logging.warning(dep_ids)
        logging.warning(emp_ids)

        # for i in records_ids:
        #     logging.warning(i.record_dep.name)




        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env['mrp.production.record'].browse(self._ids),
            'div_qty':div_qty,
            'dep_ids':dep_ids,
            'emp_ids':emp_ids

            }
        return self.env['report'].render('mrp_prod.mrp_prod_record_qweb', docargs)