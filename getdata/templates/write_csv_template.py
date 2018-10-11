{% load getdata_extras %}SNUM,{% for f in fields %}"{{f|addslashes}}",{% endfor %}{% for f in fields_anat %}"{{f|addslashes}}",{% endfor %}
{% for subj,vals_anat in subj_data_tuples %}
"{{subj.snum|addslashes}}",{% for f in fields %}"{{ subj|getattribute:f|addslashes }}",{% endfor %}{% for v in vals_anat %}"{{ v.value|addslashes }}",{% endfor %}	
{% endfor %}

