# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging
from openerp.exceptions import ValidationError





class mrp_prod_workcenter(models.Model):

    _name = 'mrp.workcenter'
    _inherit = ['mrp.workcenter']

    @api.multi
    @api.depends('time_cycle', 'capacity_per_cycle')
    def _compute_workcenter_eff(self):
        self.workcenter_eff = (self.time_cycle * 3600.00) / self.capacity_per_cycle



    workcenter_eff=fields.Float(string='Work Center Efficiency',compute='_compute_workcenter_eff' ,store=True)
    workcenter_dep = fields.Many2one(comodel_name='mrp.dep', string='MNF Department')
    record_ids=fields.One2many(comodel_name="mrp.production.record",inverse_name="workcenter_id",string="Production Records")

class mrp__prod_department(models.Model):
    _name = 'mrp.dep'
    name = fields.Char(string='Manufacturing Department')

    sequence=fields.Integer(string="sequence")
    workcenter_ids = fields.One2many(comodel_name="mrp.workcenter", inverse_name="workcenter_dep", string="WorkCenters",
                                 required=False, )
    employee_ids=fields.Many2many(comodel_name="hr.employee",relation="dep_employee_rel",column1="employee_id",column2="dep_id",string="working People")
    record_ids=fields.One2many(comodel_name="mrp.production.record",inverse_name="record_dep",string="Production Records")



class mrp_prod_production_workcenter_line(models.Model):


    _name = 'mrp.production.workcenter.line'
    _inherit = ['mrp.production.workcenter.line']

    @api.multi
    @api.depends('hour','cycle')
    def _compute_operation_coff(self):
        if self.hour ==0:
            return
        else:
            self.production_coff = int(self.cycle/self.hour)
            #self.production_coff= ( self.hour * 3600 ) / self.cycle


    @api.onchange('record_ids')
    def _compute_remaining_products(self):
        total=0

        for record in self.record_ids:
            total =total+record.pro_qty
        self.rem_qty=self.qty-total
        # raise Warning(_('work order changed'))




    record_ids=fields.One2many(comodel_name='mrp.production.record',inverse_name='workorder_id',string='Record')
    production_coff=fields.Float(string='Calibration Value',compute='_compute_operation_coff')
    dep_id=fields.Many2one(comodel_name='mrp.dep',string="MNF Department")
    rem_qty=fields.Integer(string="Remaining Quantity" ,compute='_compute_remaining_products')
    hour=fields.Float('Number of Hours', digits=(16, 5))


class mrp_prod_production_record(models.Model):
    _name = 'mrp.production.record'

    @api.multi
    @api.depends('time_taken','pro_qty')
    def _compute_eff(self):
        if (self.workorder_id.production_coff ==0) or (self.time_taken == 0)  :
            return
        else:

            self.pro_ef = ( ( self.pro_qty / self.time_taken ) / self.workorder_id.production_coff ) * 100
            #self.pro_ef= (self.workorder_id.production_coff * 100 ) /((self.time_taken * 3600.00) /float(self.pro_qty))



    # @api.one
    # @api.onchange('workcenter_id')
    # def onchange_dep(self):
    #     self.record_dep=self.workcenter_id.workcenter_dep
    #     #raise Warning(_('work center chabged '))

    @api.one
    @api.onchange('workorder_id')
    def onchange_workorder(self):
        self.mnforder_id = self.workorder_id.production_id
        self.workcenter_id = self.workorder_id.workcenter_id
        self.record_dep = self.workcenter_id.workcenter_dep

        #raise Warning(_('work order changed'))

    # @api.one
    # @api.depends('pro_qty')
    # def _compute_record_rem_qty(self):
    #     self.rem_qty=self.rem_qty-self.pro_qty
    #     logging.warning(self.workorder_id.rem_qty)


    @api.one
    @api.depends('pro_qty')
    def _compute_rem_qty(self):
        self.rem_qty=self.workorder_id.rem_qty

        logging.warning(self.workorder_id.rem_qty)





    @api.constrains('pro_qty')
    def _check_pro_qty(self):



        if self.rem_qty < 0 :
            logging.warning(self.workorder_id.rem_qty)
            raise ValidationError("Quantity Must be less than or equal to work order remaining Quantity")


        if self.pro_qty <= 0:

            raise ValidationError("Please Enter avalid Quantity")


    @api.onchange('record_dep')
    def onchange_rec_dep(self):
        res = {}

            # self.record_dep.workcenter_ids
        res['domain'] = {'workcenter_id': [('id', 'in' , self.record_dep.workcenter_ids.ids)]}
        logging.warning("dep_id =%s" % self.record_dep)
        logging.warning(res)
        return res



           # res['domain'] = {'mnforder_': [('id', 'in', self.record_dep.workcenter_ids.ids)]}





    name=fields.Date(string='Record Date',index=True,required="True")
    workcenter_id=fields.Many2one(comodel_name='mrp.workcenter',string='Work Center',required="True")
    pro_qty=fields.Integer(string="Quantity",required="True")
    time_taken=fields.Float(string='Time',default='1.00',required="True")
    workorder_id=fields.Many2one(comodel_name="mrp.production.workcenter.line",string="workorder" ,required="True")
    mnforder_id=fields.Many2one(comodel_name="mrp.production",string="MNF Order" ,required="True")
    employee_id=fields.Many2one(comodel_name='hr.employee',string='Employee Name',index=True , required="True")
    pro_ef=fields.Float(string='EFF',compute='_compute_eff',store=True)
    record_dep=fields.Many2one(comodel_name='mrp.dep',string='MNF Department',required="True")
    rem_qty=fields.Integer(string="Remaining Quantity" ,compute='_compute_rem_qty' )




class mrp_prod_hr(models.Model):
    _name='hr.employee'
    _inherit ='hr.employee'
    records_ids=fields.One2many(comodel_name='mrp.production.record',inverse_name='employee_id',string='Employee Records')
    dep_id=fields.Many2one(comodel_name="mrp.dep")

















