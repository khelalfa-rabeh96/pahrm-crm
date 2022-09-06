from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import datetime
import customers 


from prescriptions.models import ChronicPrescription, PrescriptionItem
from customers.models import Customer


class PrescriptionItemModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="John Doe")

    def test_item_related_to_prescription(self):
        presc1 = ChronicPrescription.objects.create(customer=self.customer)
        item1 = PrescriptionItem.objects.create(drug_name="Aprovel 300 mg b/30", quantity=5, prescription=presc1)
        self.assertIn(item1, presc1.drugs.all())

        presc2 = ChronicPrescription.objects.create(customer=self.customer)
        item2 = PrescriptionItem.objects.create(drug_name="Novoformine 850 mg b/30", quantity=5, prescription=presc2)
        self.assertIn(item2, presc2.drugs.all())

        self.assertNotIn(item1, presc2.drugs.all())
        self.assertNotIn(item2, presc1.drugs.all())
    

    def test_unique_drug_name_in_the_same_prescription(self):
        presc1 = ChronicPrescription.objects.create(customer=self.customer)
        item1 = PrescriptionItem.objects.create(drug_name="Amarel 1 mg b/30", quantity=5, prescription=presc1)
        item2 = PrescriptionItem(drug_name="Amarel 1 mg b/30", quantity=51, prescription=presc1)

        with self.assertRaises(IntegrityError):
            item2.save()
            item2.full_clean()
    
    def test_same_drug_name_in_different_prescriptions(self):
        presc1 = ChronicPrescription.objects.create(customer=self.customer)
        presc2 = ChronicPrescription.objects.create(customer=self.customer)
        item1 = PrescriptionItem.objects.create(drug_name="Amarel 1 mg b/30", quantity=5, prescription=presc1)
        item2 = PrescriptionItem.objects.create(drug_name="Amarel 1 mg b/30", quantity=51, prescription=presc2)

        self.assertEqual(PrescriptionItem.objects.all().count(), 2)
    
    def test_quantity_quantity_lower_bound(self):
        presc1 = ChronicPrescription.objects.create(customer=self.customer)
        item1 = PrescriptionItem(drug_name="Amarel 1 mg b/30", quantity=0, prescription=presc1)

        with self.assertRaises(ValidationError):
            item1.save()
            item1.full_clean()



class ChronicPrescriptionModelTest(TestCase):
    
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="John Doe")

    def test_default_duration(self):
        chronicPresc = ChronicPrescription.objects.create(customer=self.customer)
        duration = chronicPresc.duration
        self.assertEqual(duration, 90)
    
    def test_max_duration(self):
        chronicPresc = ChronicPrescription(duration=100, customer=self.customer)
       # Should raise an error cause max duration is 90
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_min_duration(self):
        chronicPresc = ChronicPrescription(duration=29, customer=self.customer)
       # Should raise an error cause min duration is 30
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_default_notificationStatus(self):
        chronicPresc = ChronicPrescription.objects.create(customer=self.customer)
        notification_status = chronicPresc.notification_status
        self.assertTrue(notification_status)
    

    def test_date_upper_bound(self):
        future_date = datetime.date.today() +  datetime.timedelta(days=1)
        chronicPresc = ChronicPrescription(date=future_date, customer=self.customer)
        
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_date_lower_bound(self):
        old_date = datetime.date.today() - datetime.timedelta(days=91)
        chronicPresc = ChronicPrescription(date=old_date, customer=self.customer)
        
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_count_left_days(self):
        presc = ChronicPrescription(date=datetime.date(2022,3,1), duration=45, customer=self.customer)

        # Since Mars got 31 days
        expected_serving_day = datetime.date(2022,4,15)
        left_days = presc.count_left_days()
        print(left_days)

        self.assertEqual(datetime.date.today()+datetime.timedelta(days=left_days), expected_serving_day)
