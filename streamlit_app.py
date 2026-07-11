# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders! :cup_with_straw: ")
st.write(  """Order that need to be filled.  """)


session = get_active_session()
#my_dataframe = session.table("smoothies.public.orders").
#select(col('NAME_ON_ORDER')).select col('ORDER_FILLED')
#st.dataframe(data=my_dataframe, use_container_width=True)

#my_dataframe = session.table("smoothies.public.orders").select(col('NAME_ON_ORDER'), col('ORDER_FILLED'),select(col('INGREDIENTS'),select(col('ORDER_TS')

my_dataframe = session.table("smoothies.public.orders").select(col('NAME_ON_ORDER'), col('ORDER_FILLED'), col('INGREDIENTS'), col('ORDER_TS'))



#my_dataframe = session.table("smoothies.public.orders").select(col('NAME_ON_ORDER'), col('ORDER_FILLED'))
editable_df = st.data_editor(my_dataframe)

submitted = st.button('Submit')

if submitted:
    st.success("Someone clicked the button",icon = '👍')
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
