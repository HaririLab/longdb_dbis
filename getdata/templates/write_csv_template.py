{% load getdata_extras %}SNUM,{% for f in fields %}"{{f|addslashes}}",{% endfor %}{% for f in seq_names %}"{{f|addslashes}}"_inclusive,"{{f|addslashes}}"_strict,"{{f|addslashes}}"_notes,{% endfor %}{% for f in fields_hcpmpp %}"{{f|addslashes}}",{% endfor %}
{% for subj,vals_inc,vals_hcpmpp,vals_funcROImean, vals_freesurfer in subj_data_tuples %}"{{subj.snum|addslashes}}",{% for f in fields %}"{{ subj|getattribute:f|addslashes }}",{% endfor %}{% for v in vals_inc %}"{{ v.inclusive|addslashes }}","{{ v.strict|addslashes }}","{{ v.note|addslashes }}",{% endfor %}{% for v in vals_hcpmpp %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_funcROImean %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_freesurfer %}"{{ v.value|addslashes }}",{% endfor %}
{% endfor %}

