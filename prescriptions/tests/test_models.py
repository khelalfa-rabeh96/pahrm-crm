from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import datetime 


from prescriptions.models import ChronicPrescription, PrescriptionItem

class PrescriptionItemModelTest(TestCase):

    def test_item_related_to_prescription(self):
        presc1 = ChronicPrescription.objects.create()
        item1 = PrescriptionItem.objects.create(drug_name="Aprovel 300 mg b/30", quantity=5, prescription=presc1)
        self.assertIn(item1, presc1.drugs.all())

        presc2 = ChronicPrescription.objects.create()
        item2 = PrescriptionItem.objects.create(drug_name="Novoformine 850 mg b/30", quantity=5, prescription=presc2)
        self.assertIn(item2, presc2.drugs.all())

        self.assertNotIn(item1, presc2.drugs.all())
        self.assertNotIn(item2, presc1.drugs.all())
    
    def test_unique_item_by_name(self):
        presc1 = ChronicPrescription.objects.create()
        item1 = PrescriptionItem.objects.create(drug_name="Amarel 1 mg b/30", quantity=5, prescription=presc1)
        item2 = PrescriptionItem(drug_name="Amarel 1 mg b/30", quantity=51, prescription=presc1)

        with self.assertRaises(IntegrityError):
            item2.save()
            item2.full_clean()
    
    def test_quantity_quantity_lower_bound(self):
        presc1 = ChronicPrescription.objects.create()
        item1 = PrescriptionItem(drug_name="Amarel 1 mg b/30", quantity=0, prescription=presc1)

        with self.assertRaises(ValidationError):
            item1.save()
            item1.full_clean()


    

    





class ChronicPrescriptionModelTest(TestCase):
    

    def test_defaultduration(self):
        chronicPresc = ChronicPrescription.objects.create()
        duration = chronicPresc.duration
        self.assertEqual(duration, 90)
    
    def test_max_duration(self):
        chronicPresc = ChronicPrescription(duration=100)
       # Should raise an error cause max duration is 90
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_min_duration(self):
        chronicPresc = ChronicPrescription(duration=29)
       # Should raise an error cause min duration is 30
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_default_notificationStatus(self):
        chronicPresc = ChronicPrescription.objects.create()
        notification_status = chronicPresc.notification_status
        self.assertTrue(notification_status)
    

    def test_date_upper_bound(self):
        future_date = datetime.date.today() +  datetime.timedelta(days=1)
        chronicPresc = ChronicPrescription(date=future_date)
        
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()
    
    def test_date_lower_bound(self):
        old_date = datetime.date.today() - datetime.timedelta(days=91)
        chronicPresc = ChronicPrescription(date=old_date)
        
        with self.assertRaises(ValidationError):
            chronicPresc.save()
            chronicPresc.full_clean()

