import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import classes from './RegisterGroupList.module.css';
import LineChart from '../components/Report/LineChart';
import ReportConfigButtonForm from '../components/Report/ReportConfigButtonForm';

const returnEleConfig = (register_type, meassures) => {
  const created_at = [];
  const listE1 = [];
  const listW1 = [];
  const listVrms1 = [];
  const listIrms1 = [];
  const listVA1 = [];
  const listFP1 = [];

  const listE2 = [];
  const listW2 = [];
  const listVrms2 = [];
  const listIrms2 = [];
  const listVA2 = [];
  const listFP2 = [];

  const listE3 = [];
  const listW3 = [];
  const listVrms3 = [];
  const listIrms3 = [];
  const listVA3 = [];
  const listFP3 = [];

  meassures.forEach((element) => {
    created_at.push(element.created_at);

    listE1.push(element.e1);
    listW1.push(element.w1);
    listVrms1.push(element.vrms1);
    listIrms1.push(element.irms1);
    listVA1.push(element.va1);
    listFP1.push(element.fp1);

    if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
      listE2.push(element.e2);
      listW2.push(element.w2);
      listVrms2.push(element.vrms2);
      listIrms2.push(element.irms2);
      listVA2.push(element.va2);
      listFP2.push(element.fp2);
    }

    if (register_type === 'ENERGY3') {
      listE3.push(element.e3);
      listW3.push(element.w3);
      listVrms3.push(element.vrms3);
      listIrms3.push(element.irms3);
      listVA3.push(element.va3);
      listFP3.push(element.fp3);
    }
  });

  const dataE = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listE1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataE.datasets.push({
      label: 'Fase 2',
      data: listE2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataE.datasets.push({
      label: 'Fase 3',
      data: listE3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }

  const dataW = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listW1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataW.datasets.push({
      label: 'Fase 2',
      data: listW2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataW.datasets.push({
      label: 'Fase 3',
      data: listW3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }

  const dataVrms = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listVrms1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataVrms.datasets.push({
      label: 'Fase 2',
      data: listVrms2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataVrms.datasets.push({
      label: 'Fase 3',
      data: listVrms3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }

  const dataIrms = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listIrms1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataIrms.datasets.push({
      label: 'Fase 2',
      data: listIrms2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataIrms.datasets.push({
      label: 'Fase 3',
      data: listIrms3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }

  const dataVA = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listVA1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataVA.datasets.push({
      label: 'Fase 2',
      data: listVA2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataVA.datasets.push({
      label: 'Fase 3',
      data: listVA3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }

  const dataFP = {
    labels: created_at,
    datasets: [
      {
        label: 'Fase 1',
        data: listFP1,
        fill: false,
        borderColor: 'rgb(100, 190, 75)',
        tension: 0.1,
      },
    ],
  };
  if (register_type === 'ENERGY2' || register_type === 'ENERGY3') {
    dataFP.datasets.push({
      label: 'Fase 2',
      data: listFP2,
      fill: false,
      borderColor: 'rgb(192, 75, 75)',
      tension: 0.1,
    });
  }
  if (register_type === 'ENERGY3') {
    dataFP.datasets.push({
      label: 'Fase 3',
      data: listFP3,
      fill: false,
      borderColor: 'rgb(75, 83, 192)',
      tension: 0.1,
    });
  }
  return [dataE, dataW, dataVrms, dataIrms, dataVA, dataFP];
};

const ReportPage = () => {
  const location = useLocation();

  const register = location.state.register;
  const [meassures, setMeassures] = useState(location.state.meassures);
  const [openReportModal, setOpenReportModal] = useState(false);

  const [dataE, dataW, dataVrms, dataIrms, dataVA, dataFP] = returnEleConfig(
    register.register_type,
    meassures
  );

  return (
    <section>
      <header className={classes.headerTopic}>
        <div id="localNavigation">
          <Link
            to={{
              pathname: '/alarms',
            }}
          >
            Alarms
          </Link>
          {'>'}
          <Link
            to={{
              pathname: '/registerGroups',
            }}
          >
            Grupos
          </Link>
          {'>'}
          <Link
            to={{
              pathname: '/registersList',
              state: { regGroupId: register.register_group_id },
            }}
          >
            Medidores
          </Link>
          {'>'}
          <Link
            to={{
              pathname: '/registersMeassures',
              state: {
                register_id: register.id,
                group_id: register.register_group_id,
              },
            }}
          >
            Medidores
          </Link>
          {'>'}
        </div>

        <h1 className={classes.h1}>Gráficos</h1>
        <div>
          <button
            className={classes.openModalBtn}
            onClick={() => setOpenReportModal(true)}
          >
            Mostrar Gráficos
          </button>
          {openReportModal && (
            <ReportConfigButtonForm
              closeModal={setOpenReportModal}
              regId={register.id}
              groupId={register.group_id}
              setMeassures={setMeassures}
            />
          )}
        </div>
      </header>
      <div>
        <div>
          <h3 className={classes.h3}>Energia consumida instantânea [kwh]</h3>
          <LineChart chartData={dataE} />
        </div>
        <div>
          <h3 className={classes.h3}>Potência ativa [W]</h3>
          <LineChart chartData={dataW} />
        </div>
        <div>
          <h3 className={classes.h3}>Tensão Vrms [V]</h3>
          <LineChart chartData={dataVrms} />
        </div>
        <div>
          <h3 className={classes.h3}>Corrente Irms [V]</h3>
          <LineChart chartData={dataIrms} />
        </div>
        <div>
          <h3 className={classes.h3}>Potência Aparente [VA]</h3>
          <LineChart chartData={dataVA} />
        </div>
        <div>
          <h3 className={classes.h3}>Fator de potencia</h3>
          <LineChart chartData={dataFP} />
        </div>
      </div>
    </section>
  );
};

export default ReportPage;
