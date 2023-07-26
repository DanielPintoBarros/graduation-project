import classes from './MeassureItem.module.css';
import AuthContext from '../../store/auth-context';
import { useState, useContext, useEffect } from 'react';

const schemaEnergy1 = (args) => {
  return (
    <li className={classes.item1}>
      <div className={classes.content}>
        <div>
          <p className={classes.row}>
            <b>E1</b> = {args.E1.toFixed(3)} [kWh]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Vrms1</b> = {args.vrms1.toFixed(3)} [V]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Irms1</b> = {args.irms1.toFixed(3)} [A]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>W1</b> = {args.w1.toFixed(3)} [W]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>VA1</b> = {args.va1.toFixed(3)} [VA]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>fp1</b> = {args.fp1.toFixed(3)}
          </p>
        </div>
      </div>
    </li>
  );
};

const schemaEnergy2 = (args) => {
  return (
    <li className={classes.item2}>
      <div className={classes.content}>
        <div>
          <p className={classes.row}>
            <b>E1</b> = {args.E1.toFixed(3)} [kWh]
          </p>
          <p className={classes.row}>
            <b>E2</b> = {args.E2.toFixed(3)} [kWh]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Vrms1</b> = {args.vrms1.toFixed(3)} [V]
          </p>
          <p className={classes.row}>
            <b>Vrms2</b> = {args.vrms2.toFixed(3)} [V]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Irms1</b> = {args.irms1.toFixed(3)} [A]
          </p>
          <p className={classes.row}>
            <b>Irms2</b> = {args.irms2.toFixed(3)} [A]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>W1</b> = {args.w1.toFixed(3)} [W]
          </p>
          <p className={classes.row}>
            <b>W2</b> = {args.w2.toFixed(3)} [W]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>VA1</b> = {args.va1.toFixed(3)} [VA]
          </p>
          <p className={classes.row}>
            <b>VA2</b> = {args.va2.toFixed(3)} [VA]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>fp1</b> = {args.fp1.toFixed(3)}
          </p>
          <p className={classes.row}>
            <b>fp2</b> = {args.fp2.toFixed(3)}
          </p>
        </div>
      </div>
    </li>
  );
};

const schemaEnergy3 = (args) => {
  return (
    <li className={classes.item3}>
      <div className={classes.content}>
        <div>
          <p className={classes.row}>
            <b>E1</b> = {args.e1.toFixed(3)} [kWh]
          </p>
          <p className={classes.row}>
            <b>E2</b> = {args.e2.toFixed(3)} [kWh]
          </p>
          <p className={classes.row}>
            <b>E3</b> = {args.e3.toFixed(3)} [kWh]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Vrms1</b> = {args.vrms1.toFixed(3)} [V]
          </p>
          <p className={classes.row}>
            <b>Vrms2</b> = {args.vrms2.toFixed(3)} [V]
          </p>
          <p className={classes.row}>
            <b>Vrms3</b> = {args.vrms3.toFixed(3)} [V]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>Irms1</b> = {args.irms1.toFixed(3)} [A]
          </p>
          <p className={classes.row}>
            <b>Irms2</b> = {args.irms2.toFixed(3)} [A]
          </p>
          <p className={classes.row}>
            <b>Irms3</b> = {args.irms3.toFixed(3)} [A]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>W1</b> = {args.w1.toFixed(3)} [W]
          </p>
          <p className={classes.row}>
            <b>W2</b> = {args.w2.toFixed(3)} [W]
          </p>
          <p className={classes.row}>
            <b>W3</b> = {args.w3.toFixed(3)} [W]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>VA1</b> = {args.va1.toFixed(3)} [VA]
          </p>
          <p className={classes.row}>
            <b>VA2</b> = {args.va2.toFixed(3)} [VA]
          </p>
          <p className={classes.row}>
            <b>VA3</b> = {args.va3.toFixed(3)} [VA]
          </p>
        </div>
        <div>
          <p className={classes.row}>
            <b>fp1</b> = {args.fp1.toFixed(3)}
          </p>
          <p className={classes.row}>
            <b>fp2</b> = {args.fp2.toFixed(3)}
          </p>
          <p className={classes.row}>
            <b>fp3</b> = {args.fp3.toFixed(3)}
          </p>
        </div>
      </div>
    </li>
  );
};
const schemaWater = (args) => {
  return (
    <li className={classes.item2}>
      <div className={classes.content}>
        <div>
          <p className={classes.row}>
            <b>Consumo</b> = {args.water_consume.toFixed(3)}
          </p>
        </div>
      </div>
    </li>
  );
};

const MeassureItem = (props) => {
  const authCtx = useContext(AuthContext);
  const [meassure, setMeassure] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [firstAccess, setFirstAccess] = useState(true);

  useEffect(() => {
    if (!isLoading && props.refresh) {
      setTimeout(() => {
        setIsLoading(true);
      }, 10000);
    }
  });

  function fetchRegistersMeassure() {
    fetch(`/api/register/${props.register_id}/lastMeassure`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((response) => {
      return response.json().then((data) => {
        setMeassure(data.meassure);
        setIsLoading(false);
        setFirstAccess(false);
      });
    });
  }

  if (isLoading) {
    fetchRegistersMeassure();
  }

  return (
    <div>
      {firstAccess && isLoading && (
        <div className={classes.content}>Loading...</div>
      )}
      {!firstAccess && Object.keys(meassure).length > 0 && (
        <div>
          {props.register_type === 'ENERGY1' && schemaEnergy1(meassure)}
          {props.register_type === 'ENERGY2' && schemaEnergy2(meassure)}
          {props.register_type === 'ENERGY3' && schemaEnergy3(meassure)}
          {props.register_type === 'WATER' && schemaWater(meassure)}
        </div>
      )}
      {!firstAccess && Object.keys(meassure).length === 0 && (
        <div className={classes.content}>Nenhuma medida foi encontrada</div>
      )}
    </div>
  );
};

export default MeassureItem;
