import { useState, useEffect } from "react";
import FormData from 'form-data'
import { useDispatch } from "react-redux";
import Form from 'react-bootstrap/Form';
import { getLabelsNames, getMemes, postLabel } from '../../utils/requests';
import { setMemes } from '../../slices/memesSlice';
import CreatableSelect from 'react-select/creatable';

const LabelPostForm = ({ meme }) => {
  const [labelNames, setLabelNames] = useState([]);

  const [inputValue, setInputValue] = useState('');
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();

  // get label names
  useEffect(() => {
    const inner = async () => {
      try {
        const labelNamesFromDb = await getLabelsNames(access_token)
        const optionsList = labelNamesFromDb.map((labelName) => {
          return { value: labelName, label: labelName }
        })
        setLabelNames(optionsList)
        
      } catch (e) {
        console.log('labels get error');
        console.log(e)
      }      
    }
    inner();
  }, []);

  // Function triggered on selection
  const handleSelect = async (data) => {
    if (data) {
      const form = new FormData();
      form.append('title', data.value);
      form.append('meme_id', meme.id);

      await postLabel(form, access_token);
      const getMemesResponse = await getMemes(access_token);
      dispatch(setMemes(getMemesResponse.data))      
    }
  }

  return <CreatableSelect 
          isClearable 
          options={labelNames}
          placeholder="Напишите смешной тег"
          onChange={handleSelect}
          isSearchable={true}
        />
}

export default LabelPostForm;