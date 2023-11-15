export default function PropertyDetails({ data } : { data: any}) {
    
    const percentage: number = Math.round((data.total_amount_paid / data.purchase_price) * 100);

    return (
        <div className="header">
            <h1>{data.full_address}</h1>
            Ownership
            <h2>
                You own about <span className="info">{percentage}% </span>
                or <span className="info">£{data.total_amount_paid} </span>
                at the current valuation of <span className="info">£{data.purchase_price}</span>
            </h2>
        </div>
    )
  }