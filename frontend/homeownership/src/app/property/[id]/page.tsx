'use client';

import BuyNow from "@/components/BuyNow"
import PropertyDetails from "@/components/PropertyDetails"
import { useCallback, useEffect, useState } from "react";
import { useRouter } from 'next/navigation';


export default function Page({ params }: { params: { id: string } }) {
  const [data, setData] = useState<Object | null>(null);
  const router = useRouter();
  
  const fetchData = useCallback(async () => {
    const res = await fetch(`http://127.0.0.1:8000/api/properties/${params.id}/`);
    
    if (!res.ok) {
      router.push(`/error404`);
    } else {
      setData(await res.json());
    }
  }, [params.id, router]);
  
  useEffect(() => {

      fetchData();

  }, [fetchData]);

  const submitHandler = () => {
    fetchData();
  };

  return (
  <div>
       {data && <PropertyDetails data={data}></PropertyDetails>}
       {data && <BuyNow propertyId={params.id} submitHandler={submitHandler}></BuyNow>}
  </div>
  )
}