import { useLocation } from 'react-router-dom';
import classes from './RegisterGroupList.module.css';
import RegistersComponent from '../components/Register/RegistersComponent';
import MeassureItem from '../components/Meassure/MeassureItem';

const MeassureRegisterPage = () => {
  const location = useLocation();

  const register = location.state.register;

  return (
    <section>
      <div>
        <h1 className={classes.h1}>Medidor</h1>
        <ul className={classes.list}>
          <RegistersComponent
            key={register.id}
            register={register}
            center={true}
          />
        </ul>
        <h1 className={classes.h1}>Última medida</h1>
        <ul className={classes.list}>
          <MeassureItem
            key={register.id}
            register_id={register.id}
            register_type={register.register_type}
          />
        </ul>
      </div>
    </section>
  );
};

export default MeassureRegisterPage;
